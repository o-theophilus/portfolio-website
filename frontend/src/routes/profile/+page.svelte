<script>
	import { page } from '$app/stores';
	import { user as me, module, portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Icon from '$lib/icon.svelte';
	import BRound from '$lib/button/round.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Log from '$lib/log.svelte';

	import Photo from './_photo.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Email from './_email.svelte';
	import Delete from './_delete.svelte';
	import Password from './_password.svelte';
	import Permission from './permission.svelte';

	export let data;
	$: user = data.user;
	let { permissions } = data;
	let edit_mode = false;

	$: if ($portal) {
		if ($portal.for == 'user') {
			user = $portal.data;
			if (user.key == $me.key) {
				$me = user;
			}
		} else if ($portal.for == 'photo') {
			user.photo = $portal.data;
			if (user.key == $me.key) {
				$me = user;
			}
		}

		$portal = {};
	}
</script>

{#key `${$page.url.pathname}${$page.url.search}`}
	<Meta title={user?.name || data.error} />
	<!-- <Meta title={user.name} description="This page includes the user profile" /> -->

	{#if user}
		<Log
			action={'viewed'}
			entity_key={user.key}
			entity_type={'user'}
		/>
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

			{#if user.key == $me.key}
				<Toggle
					state_1="off"
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
			{#if edit_mode}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Photo,
							user
						};
					}}
				/>
			{/if}
		</div>

		<br />

		<div class="line">
			<Icon icon="person" size="20" />
			<strong class="ititle">
				{user.name}
			</strong>
			{#if edit_mode}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Name,
							user
						};
					}}
				/>
			{/if}
		</div>

		<div class="line">
			<Icon icon="email" size="20" />
			{user.email}

			{#if edit_mode}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Email,
							user
						};
					}}
				/>
			{/if}
		</div>

		<div class="line">
			<Icon icon="phone" size="20" />
			{user.phone || 'None'}
			{#if edit_mode}
				<BRound
					icon="edit"
					on:click={() => {
						$module = {
							module: Phone,
							user
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
							module: Password,
							user
						};
					}}
				>
					<Icon icon="phone" size="20" />
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
					<Icon icon="delete" size="20" />
					Delete Account
				</Button>
			</div>
		{/if}
		<br /><br /><br />

		{#if $me.permissions.includes('log:view')}
			<hr />
			<div class="pad">
				<Link href="/log?{new URLSearchParams(`search=${user.email}:all:all:`).toString()}">
					view logs
				</Link>
			</div>
		{/if}

		{#if user && user.key != $me.key && user.status == 'confirmed' && $me.permissions.includes('user:set_permission')}
			<hr />
			<Permission {user} {permissions} />
		{/if}
	{/if}
</Content>

<style>
	.title {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.ititle {
		color: var(--ft1);
		font-size: x-large;
	}

	.line {
		display: flex;
		gap: var(--sp2);
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
