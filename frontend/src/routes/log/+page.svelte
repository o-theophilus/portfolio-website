<script>
	import { replaceState } from '$app/navigation';
	import { app, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Button } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Meta } from '$lib/macro';
	import One from './one.svelte';

	let { data } = $props();
	let logs = $derived(data.logs);
	let total_page = $derived(data.total_page);
	let search_query = $derived(data.search_query);
	let searchParams = $state({ ...data.searchParams });
	let defaultParams = $state(data.searchParams);

	onMount(() => {
		const sp = page_state.searchParams;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}
	});
</script>

<Meta title="Logs" />

<Content>
	<div class="page_title">Logs</div>

	<br />

	{#if app.user.access.includes('log:view')}
		<div class="line nowrap">
			<Search
				placeholder="Search for User"
				bind:value={searchParams.u_search}
				ondone={(v) => {
					searchParams.page_no = 1;
					page_state.set({ u_search: v });
				}}
			></Search>
			<Button onclick={() => (searchParams.u_search = app.user.key)}>Me</Button>
		</div>
	{/if}

	<div class="line nowrap">
		<Dropdown
			icon2="chevron-down"
			list={Object.keys(search_query)}
			bind:value={searchParams.entity_type}
			onchange={(v) => {
				searchParams.page_no = 1;
				searchParams.action = 'all';
				page_state.set({
					entity_type: v == defaultParams.entity_type ? '' : v,
					action: ''
				});
			}}
			--select-width="100%"
		/>
		<Dropdown
			icon2="chevron-down"
			list={search_query[searchParams.entity_type]}
			bind:value={searchParams.action}
			onchange={(v) => {
				searchParams.page_no = 1;
				page_state.set({ action: v == defaultParams.action ? '' : v });
			}}
			--select-width="100%"
		/>
	</div>

	<Search
		placeholder="Search for {searchParams.entity_type}"
		bind:value={searchParams.e_search}
		ondone={(v) => {
			searchParams.page_no = 1;
			page_state.set({ e_search: v });
		}}
	></Search>

	{#each logs as log (log.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {log} bind:search={searchParams} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No log found
		</PageNote>
	{/each}

	<Pagination
		{total_page}
		bind:value={searchParams.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>
