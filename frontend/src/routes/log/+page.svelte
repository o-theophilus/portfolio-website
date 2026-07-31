<script>
	import { replaceState } from '$app/navigation';
	import { Button } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Meta } from '$lib/macro';
	import { app, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import One from './one.svelte';

	let { data } = $props();
	let logs = $derived(data.logs);
	let total_page = $derived(data.total_page);
	let search_query = $derived(data.search_query);
	let search_params = $state({ ...data.search_params });
	let default_params = $state(data.search_params);

	onMount(() => {
		const sp = page_state.search_params;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(search_params)) {
				if (sp[key]) search_params[key] = sp[key];
			}
		}
	});
</script>

<Meta title="Logs" />

<Content --content-height="auto">
	<div class="page_title">Logs</div>

	<br />

	{#if app.user.access.includes('log.view_others')}
		<div class="line nowrap">
			<Search
				placeholder="Search for User"
				bind:value={search_params.u_search}
				ondone={(v) => {
					search_params.page_no = 1;
					page_state.set({ u_search: v });
				}}
			></Search>
			<Button
				disabled={search_params.u_search == app.user.key}
				onclick={() => {
					search_params.page_no = 1;
					search_params.u_search = app.user.key;
					page_state.set({ u_search: app.user.key });
				}}>Me</Button
			>
		</div>
	{/if}

	<div class="line nowrap">
		<Dropdown
			icon2="chevron-down"
			list={Object.keys(search_query)}
			bind:value={search_params.entity_type}
			onchange={(v) => {
				search_params.page_no = 1;
				search_params.action = 'all';
				page_state.set({
					entity_type: v == default_params.entity_type ? '' : v,
					action: ''
				});
			}}
			--select-width="100%"
		/>
		<Dropdown
			icon2="chevron-down"
			list={search_query[search_params.entity_type]}
			bind:value={search_params.action}
			onchange={(v) => {
				search_params.page_no = 1;
				page_state.set({ action: v == default_params.action ? '' : v });
			}}
			--select-width="100%"
		/>
	</div>

	<Search
		placeholder="Search for {search_params.entity_type}"
		bind:value={search_params.e_search}
		ondone={(v) => {
			search_params.page_no = 1;
			page_state.set({ e_search: v });
		}}
	></Search>
</Content>

<Content --content-padding-top="1px">
	{#each logs as log (log.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {log} bind:search_params />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No log found
		</PageNote>
	{/each}

	<Pagination
		{total_page}
		bind:value={search_params.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>
