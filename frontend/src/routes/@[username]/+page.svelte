<script>
	import { page } from '$app/state';

	import { app, module, page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Meta, Icon, Avatar, Log } from '$lib/macro';
	import { RoundButton, Button, LinkArrow, Toggle } from '$lib/button';

	import Photo from '../[slug]/photo/edit.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Username from './_username.svelte';
	import Email from './email/1_email.svelte';
	import Password from './password/1_email.svelte';
	import Delete from './delete/form.svelte';
	import Access from './access/form.svelte';
	import Action from './_admin_action.svelte';
	import Block from './_block.svelte';
	import { onMount } from 'svelte';

	let { data } = $props();
	let item = $derived(data.item);
	let edit_mode = $state(false);
	let blocked = $state(true);

	onMount(async () => {
		if (app.user.access.includes('block:block')) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/blocked/${item.key}`);
			resp = await resp.json();

			if (resp.status == 200) {
				blocked = resp.blocked;
			}
		}
	});
	const udate_blocked = () => {
		blocked = true;
	};

	const update = (data) => {
		item = data;
		if (item.key == app.user.key) {
			app.user = data;
		}
	};
</script>

<Meta title={item.name} />
<Log action={'viewed'} entity_key={item.key} entity_type={'user'} />

<Content>
	<div class="line">
		<div class="page_title">Profile</div>

		{#if app.login && (item.key == app.user.key || app.user.access.some( (x) => ['user:set_access', 'user:reset_name', 'user:reset_username', 'user:reset_photo', 'block:block', 'block:unblock'].includes(x) ))}
			<Toggle
				state_2="edit"
				active={edit_mode}
				onclick={() => {
					edit_mode = !edit_mode;
				}}
			/>
		{/if}
	</div>

	<br /><br /><br />

	<div class="line center">
		<Avatar name={item.name} photo={item.photo} size="120" --avatar-border-radius="50%" />

		{#if edit_mode && item.key == app.user.key}
			<RoundButton
				icon="square-pen"
				onclick={() => {
					module.open(Photo, {
						key: item.key,
						name: item.name,
						photo: item.photo,
						type: 'user',
						slug: '/user/photo',
						update
					});
				}}
			/>
		{/if}
	</div>

	<br />

	<div class="line center">
		<Icon icon="user" />
		<div class="name">
			{item.name}
		</div>
		{#if edit_mode && item.key == app.user.key}
			<RoundButton icon="square-pen" onclick={() => module.open(Name, { update })} />
		{/if}
	</div>

	<div class="line center">
		<Icon icon="mail" />
		{item.email}
		{#if edit_mode && item.key == app.user.key}
			<RoundButton icon="square-pen" onclick={() => module.open(Email, { update })} />
		{/if}
	</div>

	{#if (edit_mode && item.key == app.user.key) || item.phone}
		<div class="line center">
			<Icon icon="phone" />
			{item.phone || 'None'}
			{#if edit_mode && item.key == app.user.key}
				<RoundButton icon="square-pen" onclick={() => module.open(Phone, { update })} />
			{/if}
		</div>
	{/if}

	{#if edit_mode && item.key == app.user.key}
		<div class="line center">
			<Icon icon="at-sign" />
			{item.username}
			<RoundButton icon="square-pen" onclick={() => module.open(Username, { update })} />
		</div>

		<div class="line center">
			<Icon icon="key-round" />
			********
			<RoundButton icon="square-pen" onclick={() => module.open(Password)} />
		</div>
	{/if}

	{#if edit_mode}
		<br />
		<div class="line center wrap">
			{#if item.key == app.user.key}
				<Button --button-font-size="0.8rem" onclick={() => module.open(Delete)}>
					<Icon icon="trash-2" />
					Delete Account
				</Button>
			{:else}
				{#if app.user.access.includes('user:set_access')}
					<Button --button-font-size="0.8rem" onclick={() => module.open(Access, { ...item })}>
						Access
					</Button>
				{/if}

				{#if app.user.access.some( (x) => ['user:reset_name', 'user:reset_username', 'user:reset_photo'].includes(x) )}
					<Button
						--button-font-size="0.8rem"
						onclick={() => module.open(Action, { ...item, update })}
					>
						Reset
					</Button>
				{/if}

				{#if app.user.access.includes('block:block')}
					<Button
						icon="lock-keyhole"
						--button-font-size="0.8rem"
						disabled={blocked}
						onclick={() => module.open(Block, { key: item.key, update: udate_blocked })}
					>
						Block{#if blocked}ed{/if}
					</Button>
				{/if}
			{/if}
		</div>
	{/if}
	<br /><br /><br />

	{#if app.user.access.includes('log:view')}
		<hr />
		<div class="pad">
			<LinkArrow
				--link-font-size="0.8rem"
				onclick={() => page_state.goto('log', { u_search: item.key })}
			>
				View Logs
			</LinkArrow>
		</div>
	{/if}
</Content>

<style>
	.name {
		font-weight: 800;
		color: var(--ft1);
		font-size: 1.2rem;
	}
	.center {
		text-align: center;
		justify-content: center;
	}

	.pad,
	hr {
		margin: var(--sp2) 0;
	}
</style>
