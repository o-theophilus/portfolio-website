<script>
	import { page } from '$app/stores';
	import { user as me, module } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Icon from '$lib/icon.svelte';
	import BRound from '$lib/button/round.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Log from '$lib/log.svelte';

	import Photo from '../[slug]/photo.edit.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Email from './_email_1.svelte';
	import Delete from './_delete.svelte';
	import Password from './_password_1_email.svelte';
	import Access from './_access.svelte';

	export let data;
	$: user = data.user;
	let edit_mode = false;

	const update = (data) => {
		user = data;
		if (user.key == $me.key) {
			$me = user;
		}
	};
</script>

{#key `${$page.url.pathname}${$page.url.search}`}
	<Meta title={user?.name || data.error} />

	{#if user}
		<Log action={'viewed'} entity_key={user.key} entity_type={'user'} />
	{:else if data.error}
		<Log
			action={'viewed'}
			entity_key={$page.url.searchParams.get('search')}
			entity_type={'user'}
			status={data.status}
		/>
	{/if}
{/key}

<Content>
	{#if data.error}
		<span class="error">
			{data.error}
		</span>
	{:else}
		<div class="title">
			<strong class="ititle">Profile </strong>

			{#if user.key == $me.key || $me.access.includes('user:edit_name')}
				<Toggle
					state_2="edit"
					active={edit_mode}
					on:click={() => {
						edit_mode = !edit_mode;
					}}
				/>
			{/if}
		</div>

		<br /><br /><br />

		<div class="line">
			<div class="avatar">
				<Avatar name={user.name} photo={user.photo} size="120" />
			</div>

			{#if edit_mode && $me.access.includes('user:edit_photo')}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Photo,
							entity: {
								key: user.key,
								name: user.name,
								photo: user.photo,
								type: 'user'
							},
							update
						};
					}}
				/>
			{/if}
		</div>

		<br />

		<div class="line">
			<Icon icon="person" size="1.4" />
			<strong class="ititle">
				{user.name}
			</strong>
			{#if edit_mode && $me.access.includes('user:edit_name')}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Name,
							user,
							update
						};
					}}
				/>
			{/if}
		</div>

		<div class="line">
			<Icon icon="email" size="1.4" />
			{user.email}

			{#if edit_mode}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Email,
							update
						};
					}}
				/>
			{/if}
		</div>

		<div class="line">
			<Icon icon="call" size="1.4" />
			{user.phone || 'None'}
			{#if edit_mode}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Phone,
							user,
							update
						};
					}}
				/>
			{/if}
		</div>

		{#if edit_mode}
			<br />
			<div class="line">
				<Button
					size="small"
					on:click={() => {
						$module = {
							module: Password
						};
					}}
				>
					<Icon icon="key" size="1.4" />
					Change Password
				</Button>

				<Button
					size="small"
					on:click={() => {
						$module = {
							module: Delete,
							user
						};
					}}
				>
					<Icon icon="delete" size="1.4" />
					Delete Account
				</Button>
			</div>
		{/if}
		<br /><br /><br />

		{#if $me.access.includes('log:view')}
			<hr />
			<div class="pad">
				<Link href="/log?{new URLSearchParams(`search=${user.email}:all:all:`).toString()}">
					View Logs
				</Link>
			</div>
		{/if}

		{#if user && user.key != $me.key && user.status == 'confirmed' && $me.access.includes('user:set_access')}
			<div class="pad">
				<Link
					on:click={() => {
						$module = {
							module: Access
						};
					}}
				>
					Edit Access
				</Link>
			</div>
		{/if}
	{/if}
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

	.avatar {
		outline: 8px solid var(--bg2);
		border-radius: 50%;
		line-height: 0;
	}

	.pad,
	hr {
		margin: var(--sp2) 0;
	}
</style>
