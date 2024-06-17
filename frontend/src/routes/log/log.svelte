<script>
	import { user } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';
	import { state } from '$lib/store.js';

	import Datetime from '$lib/datetime.svelte';

	let emit = createEventDispatcher();
	export let log;

	let href = '';
	if (log.entity_type == 'post') {
		href = `/${log.entity_key}`;
	} else if (log.entity_type == 'report') {
		href = `/admin/report?search=${log.entity_key}`;
	} else if (log.entity_type == 'page') {
		href = log.entity_key;
	} else if (['user', 'admin'].includes(log.entity_type) && log.entity_key) {
		href = `/profile?search=${log.entity_key}`;
	}
</script>

<section>
	<div
		class="status"
		class:good={log.status == 200}
		class:caution={![200, 400].includes(log.status)}
		class:error={log.status == 400}
	/>

	<span class="date">
		<Datetime datetime={log.date} type="date" />
		<Datetime datetime={log.date} type="time" />
	</span>
	<br />

	<a href="/profile?search={log.user_key}">
		{log.user_name}
	</a>

	{#if log.user_key && $user.permissions.includes('log:view')}
		<button
			on:click={() => {
				emit('search', { u: log.user_key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{#if log.entity_type == 'page'} viewed {:else} {log.action} {/if}

	{#if log.action == 'viewed'}
		{#if log.entity_type == 'save'}
			save
		{:else if log.entity_type == 'user' && !log.entity_key}
			profile
		{/if}
	{:else if log.entity_type == 'otp'}
		otp
	{/if}

	{#if href}
		{log.entity_type}

		<a
			{href}
			data-sveltekit-preload-data="off"
			on:click={() => {
				if (log.entity_type == 'report') {
					let pn = 'reports';
					let i = $state.findIndex((x) => x.name == pn);
					if (i != -1) {
						$state.splice(i, 1);
					}
				}
			}}
		>
			{log.entity_name}
		</a>

		<button
			on:click={() => {
				emit('search', { e: log.entity_key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{#if log.misc}
		<br />
		{#each Object.entries(log.misc) as [key, value]}
			{key}:
			{#if log.entity_type == 'voucher' && key == 'validity'}
				<Datetime datetime={value} type="date" />
			{:else}
				{value}
			{/if}
			<br />
		{/each}
	{/if}
</section>

<style>
	section {
		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--bg2);
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		background-color: var(--cl5);
		color: var(--ac6_);
	}
	.good {
		background-color: var(--cl3);
	}
	.caution {
		background-color: var(--cl4);
	}
	.error {
		background-color: var(--cl2);
	}

	.date {
		font-size: smaller;
		color: var(--ft2);
	}

	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 700;
	}
	button {
		color: var(--cl1);
		border: none;
		background-color: transparent;
		cursor: pointer;
	}

	button:hover,
	a:hover {
		color: var(--cl1_b);
	}
</style>
