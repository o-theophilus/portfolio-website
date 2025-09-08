<script>
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Meta, Icon, Avatar, Log } from '$lib/macro';
	import { RoundButton, Button, LinkArrow, Toggle } from '$lib/button';

	import Photo from '../[slug]/photo/edit.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Email from './_email_1.svelte';
	import Username from './_username.svelte';
	import Delete from './_delete_1_warning.svelte';
	import Password from './_password_1_email.svelte';
	import Access from './_access.svelte';
	import Action from './_admin_action.svelte';
	import Block from './_admin_block.svelte';

	let { data } = $props();
	let user = $derived(data.user);
	let edit_mode = $state(false);

	const ppt = ['user:set_access', 'user:reset_name', 'user:reset_photo', 'user:block'];
	let is_admin = $derived.by(() => {
		for (const x of ppt) if (app.user.access.includes(x)) return true;
		return false;
	});

	const update = (data) => {
		user = data;
		if (user.key == app.user.key) {
			app.user = data;
		}
	};
</script>

<Meta title={user.name} />
<Log action={'viewed'} entity_key={user.key} entity_type={'user'} />

<Content>
	<div class="line">
		<div class="page_title">Profile</div>

		{#if app.login && (user.key == app.user.key || is_admin)}
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
		<Avatar name={user.name} photo={user.photo} size="120" --avatar-border-radius="50%" />

		{#if edit_mode && user.key == app.user.key}
			<RoundButton
				icon="square-pen"
				onclick={() => {
					module.open(Photo, {
						key: user.key,
						name: user.name,
						photo: user.photo,
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
			{user.name}
		</div>
		{#if edit_mode && user.key == app.user.key}
			<RoundButton icon="square-pen" onclick={() => module.open(Name, { update })} />
		{/if}
	</div>

	<div class="line center">
		<Icon icon="mail" />
		{user.email}
		{#if edit_mode && user.key == app.user.key}
			<RoundButton icon="square-pen" onclick={() => module.open(Email, { update })} />
		{/if}
	</div>

	{#if (edit_mode && user.key == app.user.key) || user.phone}
		<div class="line center">
			<Icon icon="phone" />
			{user.phone || 'None'}
			{#if edit_mode && user.key == app.user.key}
				<RoundButton icon="square-pen" onclick={() => module.open(Phone, { update })} />
			{/if}
		</div>
	{/if}

	{#if edit_mode && user.key == app.user.key}
		<div class="line center">
			<Icon icon="at-sign" />
			{user.username}
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
			{#if user.key == app.user.key}
				<Button --button-font-size="0.8rem" onclick={() => module.open(Delete)}>
					<Icon icon="trash-2" />
					Delete Account
				</Button>
			{:else if is_admin}
				{#if app.user.access.includes('user:set_access')}
					<Button --button-font-size="0.8rem" onclick={() => module.open(Access, { ...user })}>
						Access
					</Button>
				{/if}

				{#if app.user.access.some((x) => ['user:reset_name', 'user:reset_photo'].includes(x))}
					<Button
						--button-font-size="0.8rem"
						onclick={() => module.open(Action, { ...user, update })}
					>
						Reset
					</Button>
				{/if}

				{#if app.user.access.includes('user:block')}
					<Button
						--button-font-size="0.8rem"
						onclick={() => module.open(Block, { ...user, update })}
					>
						{#if user.status == 'blocked'}
							Unblock
						{:else}
							Block
						{/if}
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
				href="/log?{new URLSearchParams(`search=${user.email}:all:all:`).toString()}"
				--link-font-size="0.8rem"
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
