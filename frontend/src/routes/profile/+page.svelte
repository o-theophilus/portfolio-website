<script>
	import { user as _user, module, portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Icon from '$lib/icon.svelte';
	import BRound from '$lib/button/round.svelte';
	import Avatar from '$lib/avatar.svelte';

	import Photo from './_photo.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Email from './_email.svelte';

	let edit_mode = true;

	let self = true;
	let user = $_user;

	$: if ($portal) {
		if ($portal.for == 'user') {
			user = $portal.data;
			if (user.key == $_user.key) {
				$_user = user;
			}
		} else if ($portal.for == 'photo') {
			user.photo = $portal.data;
			if (user.key == $_user.key) {
				$_user = user;
			}
		}

		$portal = {};
	}
</script>

<Meta title={user.name} description="This page includes the user profile" />

<Content>
	<strong class="ititle">Profile</strong>

	{#if self}
		<Toggle
			state_1="off"
			state_2="edit"
			active={edit_mode}
			on:click={() => {
				edit_mode = !edit_mode;
			}}
		/>
	{/if}

	<br /><br /><br />

	<div class="line">
		<Avatar {user} size="120" profile />
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
	<br /><br /><br />

	<hr />
	<strong class="ititle">Likes</strong>
	<hr />
	<strong class="ititle">Comments</strong>
</Content>

<style>
	.ititle {
		color: var(--ac1);
		font-size: x-large;
	}

	.line {
		display: flex;
		gap: var(--sp2);
		justify-content: center;
		align-items: center;
	}
</style>
