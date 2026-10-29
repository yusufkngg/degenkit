-- Free token creation for allow-listed wallets (Solana "Create token" service fee is waived).
-- Run once in Supabase → SQL Editor. Safe to re-run.

create table if not exists free_wallets (
  wallet_address text primary key,
  note           text,
  tools          text[] not null default '{token_create}',
  created_at     timestamptz not null default now()
);

-- Nobody can read or write the table directly from the browser (no policies for anon);
-- everything goes through the functions below.
alter table free_wallets enable row level security;

-- Same passcode the admin panel already uses for set_tool_fee / get_action_logs.
create or replace function dk_admin_ok(passcode text) returns boolean
language sql immutable as $$ select passcode is not distinct from 'mp-9f3ak2x7Lq-2026' $$;

-- Public: "is this wallet free for this tool?" -> true/false only (the list itself stays private).
create or replace function is_free_wallet(p_wallet text, p_tool text default 'token_create')
returns boolean language sql security definer stable as $$
  select exists (select 1 from free_wallets where wallet_address = p_wallet and p_tool = any (tools));
$$;

create or replace function list_free_wallets(passcode text)
returns setof free_wallets language plpgsql security definer as $$
begin
  if not dk_admin_ok(passcode) then raise exception 'invalid passcode'; end if;
  return query select * from free_wallets order by created_at desc;
end; $$;

create or replace function add_free_wallet(passcode text, p_wallet text, p_note text default null)
returns void language plpgsql security definer as $$
begin
  if not dk_admin_ok(passcode) then raise exception 'invalid passcode'; end if;
  if p_wallet !~ '^[1-9A-HJ-NP-Za-km-z]{32,44}$' then raise exception 'invalid wallet address'; end if;
  insert into free_wallets (wallet_address, note) values (p_wallet, nullif(trim(p_note), ''))
  on conflict (wallet_address) do update set note = excluded.note;
end; $$;

create or replace function remove_free_wallet(passcode text, p_wallet text)
returns void language plpgsql security definer as $$
begin
  if not dk_admin_ok(passcode) then raise exception 'invalid passcode'; end if;
  delete from free_wallets where wallet_address = p_wallet;
end; $$;

grant execute on function is_free_wallet(text, text)       to anon;
grant execute on function list_free_wallets(text)          to anon;
grant execute on function add_free_wallet(text, text, text) to anon;
grant execute on function remove_free_wallet(text, text)   to anon;
grant execute on function dk_admin_ok(text)                to anon;
