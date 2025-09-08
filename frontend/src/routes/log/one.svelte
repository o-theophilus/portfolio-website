<script>
	import { app, page_state } from '$lib/store.svelte.js';
	import { Datetime, Icon } from '$lib/macro';

	let { log, search = $bindable() } = $props();

	let href = $state('');
	if (log.entity.type == 'post') {
		href = `/${log.entity.key}`;
	} else if (log.entity.type == 'report') {
		href = `/admin/report?search=${log.entity.key}`;
	} else if (log.entity.type == 'page') {
		href = log.entity.key;
	} else if (['user', 'admin'].includes(log.entity.type) && log.entity.key) {
		href = `/@${log.entity.key}`;
	} else if (log.entity.type == 'comment') {
		href = `/${log.misc.post_key}#${log.entity.key}`;
	}
</script>

<section>
	<div
		class="status"
		class:_200={log.status == '200'}
		class:_201={!['200', '400'].includes(log.status)}
		class:_400={log.status == '400'}
	></div>

	<span class="date">
		<Datetime datetime={log.date_created} type="date_numeric" />
		<Datetime datetime={log.date_created} type="time_12h" />
	</span>
	<br />

	<a href="/@{log.user.username}" class="break">
		{log.user.name}
	</a>

	{#if log.user.key && app.user.access.includes('log:view')}
		<button
			onclick={() => {
				search.page_no = 1;
				search.u_search = log.user.key;
				page_state.set({ u_search: log.user.key });
			}}
		>
			<Icon icon="square-chevron-up"></Icon>
		</button>
	{/if}

	{log.action}
	{log.entity.type}

	{#if href}
		<a class="break" {href} data-sveltekit-preload-data="off">
			{log.entity.name}
		</a>

		<button
			onclick={() => {
				search.page_no = 1;
				search.e_search = log.entity.key;
				page_state.set({ e_search: log.entity.key });
			}}
		>
			<Icon icon="square-chevron-up"></Icon>
		</button>
	{/if}

	{#if log.misc}
		{#each Object.entries(log.misc) as [key, val]}
			,
			{key}:
			{#if log.entity.type == 'voucher' && key == 'validity'}
				<Datetime datetime={val} type="date" />
			{:else}
				<span class="break">
					{val}
				</span>
			{/if}
		{/each}
	{/if}
</section>

<style>
	section {
		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--bg2);
		color: var(--ft1);

		font-size: 0.8rem;
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;
		color: var(--ac6_);
	}
	._200 {
		background-color: green;
	}
	._201 {
		background-color: var(--yellow);
	}
	._400 {
		background-color: red;
	}

	.date {
		font-size: 0.7rem;
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
