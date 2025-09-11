<script>
	import { app, page_state } from '$lib/store.svelte.js';
	import { Datetime, Icon } from '$lib/macro';

	let { item, search = $bindable() } = $props();

	let href = $state('');
	if (item.entity.type == 'post') {
		href = `/${item.entity.key}`;
	} else if (item.entity.type == 'report') {
		href = `/admin/report?search=${item.entity.key}`;
	} else if (item.entity.type == 'page') {
		href = item.entity.key;
	} else if (['user', 'admin'].includes(item.entity.type) && item.entity.key) {
		href = `/@${item.entity.key}`;
	} else if (item.entity.type == 'comment') {
		href = `/${item.misc.post_key}#${item.entity.key}`;
	}
</script>

<section>
	<div
		class="status"
		class:_200={item.status == '200'}
		class:_201={!['200', '400'].includes(item.status)}
		class:_400={item.status == '400'}
	></div>

	<span class="date">
		<Datetime datetime={item.date_created} type="date_numeric" />
		<Datetime datetime={item.date_created} type="time_12h" />
	</span>
	<br />

	<a href="/@{item.user.username}" class="break">
		{item.user.name}
	</a>

	{#if item.user.key && app.user.access.includes('log:view')}
		<button
			onclick={() => {
				search.page_no = 1;
				search.u_search = item.user.key;
				page_state.set({ u_search: item.user.key });
			}}
		>
			<Icon icon="square-chevron-up"></Icon>
		</button>
	{/if}

	{item.action}
	{item.entity.type}

	{#if href}
		<a class="break" {href} data-sveltekit-preload-data="off">
			{item.entity.name}
		</a>

		<button
			onclick={() => {
				search.page_no = 1;
				search.e_search = item.entity.key;
				page_state.set({ e_search: item.entity.key });
			}}
		>
			<Icon icon="square-chevron-up"></Icon>
		</button>
	{/if}

	{#if item.misc}
		{#each Object.entries(item.misc) as [key, val]}
			,
			{key}:
			{#if item.entity.type == 'voucher' && key == 'validity'}
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
