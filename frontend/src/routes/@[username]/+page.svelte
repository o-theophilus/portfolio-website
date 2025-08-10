<script>
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Meta, Icon2, Avatar, Log } from '$lib/macro';
	import { RoundButton, Button, Link, Toggle } from '$lib/button';

	import Photo from '../[slug]/photo.edit.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Email from './_email_1.svelte';
	import Delete from './_delete.svelte';
	import Password from './_password_1_email.svelte';
	import Access from './_access.svelte';
	import Action from './_admin_action.svelte';
	import Block from './_admin_block.svelte';

	let me = $state(app.user);
	let { data } = $props();
	let user = $derived(data.user);
	let edit_mode = $state(false);

	const ppt = ['user:set_access', 'user:reset_name', 'user:reset_photo', 'user:block'];
	let is_admin = $derived.by(() => {
		for (const x of ppt) if (me.access.includes(x)) return true;
		return false;
	});

	const update = (data) => {
		user = data;
		if (user.key == me.key) {
			me = user;
		}
	};
</script>

<Meta title={user.name} />
<Log action={'viewed'} entity_key={user.key} entity_type={'user'} />

<Content>
	<div class="title">
		<strong class="ititle">Profile </strong>

		{#if me.login && (user.key == me.key || is_admin)}
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

	<div class="line">
		<Avatar name={user.name} photo={user.photo} size="120" />

		{#if edit_mode && user.key == me.key}
			<RoundButton
				icon="edit"
				onclick={() => {
					module.open(Photo, {
						key: user.key,
						name: user.name,
						photo: user.photo,
						type: 'user',
						update
					});
				}}
			/>
		{/if}
	</div>

	<br />

	<div class="line">
		<Icon2 icon="user" />
		<strong class="ititle">
			{user.name}
		</strong>
		{#if edit_mode && user.key == me.key}
			<RoundButton
				icon="edit"
				onclick={() => {
					module.open(Name, { user, update });
				}}
			/>
		{/if}
	</div>

	<div class="line">
		<Icon2 icon="email" />
		{user.email}

		{#if edit_mode && user.key == me.key}
			<RoundButton icon="edit" onclick={() => module.open(Email, { update })} />
		{/if}
	</div>

	<div class="line">
		<Icon2 icon="call" />
		{user.phone || 'None'}
		{#if edit_mode && user.key == me.key}
			<RoundButton icon="edit" onclick={() => module.open(Phone, { ...user, update })} />
		{/if}
	</div>

	{#if edit_mode}
		<br />
		<div class="line">
			{#if user.key == me.key}
				<Button size="small" onclick={() => module.open(Password)}>
					<Icon2 icon="key" />
					Change Password
				</Button>

				<Button size="small" onclick="{() => module.open(Delete, user)}}">
					<Icon2 icon="delete" />
					Delete Account
				</Button>
			{:else if is_admin}
				{#if me.access.includes('user:set_access')}
					<Button size="small" onclick="{() => module.open(Access)}}">Access</Button>
				{/if}

				{#if me.access.some((x) => ['user:reset_name', 'user:reset_photo'].includes(x))}
					<Button
						size="small"
						onclick={() => {
							module.open(Action, { ...user, update });
						}}
					>
						Reset
					</Button>
				{/if}

				{#if me.access.includes('user:block')}
					<Button size="small" onclick={() => (module, open(Block, { ...user, update }))}>
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

	{#if me.access.includes('log:view')}
		<hr />
		<div class="pad">
			<Link
				href="/log?{new URLSearchParams(`search=${user.email}:all:all:`).toString()}"
				--link-font-size="0.8rem"
			>
				View Logs
			</Link>
		</div>
	{/if}
	<!-- {/if} -->
</Content>

<style>
	.title {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.line {
		display: flex;
		gap: var(--sp1);
		justify-content: center;
		align-items: center;
	}

	.pad,
	hr {
		margin: var(--sp2) 0;
	}
</style>
