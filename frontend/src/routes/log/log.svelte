<script>
	import { user } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';
	import { state } from '$lib/store.js';

	import Datetime from '$lib/datetime.svelte';

	let emit = createEventDispatcher();
	export let log;

	let href = '';
	if (log.entity.type == 'post') {
		href = `/${log.entity.key}`;
	} else if (log.entity.type == 'report') {
		href = `/admin/report?search=${log.entity.key}`;
	} else if (log.entity.type == 'page') {
		href = log.entity.key;
	} else if (['user', 'admin'].includes(log.entity.type) && log.entity.key) {
		href = `/profile?search=${log.entity.key}`;
	} else if (log.entity.type == 'comment') {
		href = `/${log.misc.post_key}#${log.entity.key}`;
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

	<a href="/profile?search={log.user.key}">
		{log.user.name}
	</a>

	{#if log.user.key && $user.access.includes('log:view')}
		<button
			on:click={() => {
				emit('search', { u: log.user.key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{log.action}
	{log.entity.type}

	{#if href}
		<a
			{href}
			data-sveltekit-preload-data="off"
			on:click={() => {
				if (log.entity.type == 'report') {
					let pn = 'reports';
					let i = $state.findIndex((x) => x.name == pn);
					if (i != -1) {
						$state.splice(i, 1);
					}
				}
			}}
		>
			{log.entity.name}
		</a>

		<button
			on:click={() => {
				emit('search', { e: log.entity.key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{#if log.misc}
		<br />
		{#each Object.entries(log.misc) as [key, value]}
			{key}:
			{#if log.entity.type == 'voucher' && key == 'validity'}
				<Datetime datetime={value} type="date" />
			{:else}
				<span class="break">
					{value}
				</span>
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
		font-size: 0.8rem;
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
	.break {
		word-wrap: break-word;
	}
</style>
