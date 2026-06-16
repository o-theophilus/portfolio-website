<script>
	import { replaceState } from '$app/navigation';
	import { page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import One from './one.svelte';

	let { data } = $props();
	let reports = $derived(data.reports);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { type } = data;
	let { _status } = data;
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

	const update = (a, b) => {
		reports = a;
		total_page = b;
	};
</script>

<Log entity_type={'page'} />
<Meta title="All Users" />

<Content --content-height="auto">
	<div class="page_title">
		Report{reports.length > 1 ? 's' : ''}
	</div>

	<Search
		bind:value={searchParams.search}
		ondone={(v) => {
			searchParams.page_no = 1;
			page_state.set({ search: v });
		}}
	></Search>

	<div class="line space">
		<div class="line">
			<Dropdown
				--select-height="32px"
				--select-padding-x="8px"
				--select-font-size="0.8rem"
				icon="list-filter"
				icon2="chevron-down"
				label="Type: {searchParams.type}"
				list={type}
				bind:value={searchParams.type}
				onchange={(v) => {
					searchParams.page_no = 1;
					page_state.set({ type: v == defaultParams.type ? '' : v });
				}}
			/>
			<Dropdown
				--select-height="32px"
				--select-padding-x="8px"
				--select-font-size="0.8rem"
				icon="list-filter"
				icon2="chevron-down"
				label="Status: {searchParams.status}"
				list={_status}
				bind:value={searchParams.status}
				onchange={(v) => {
					searchParams.page_no = 1;
					page_state.set({ status: v == defaultParams.status ? '' : v });
				}}
			/>
		</div>

		<Dropdown
			--select-height="1"
			--select-padding-x="0"
			--select-font-size="0.8rem"
			--select-background-color="transparent"
			--select-background-color-hover="transparent"
			--select-color="var(--ft2)"
			--select-color-hover="var(--ft1)"
			--select-outline-color="transparent"
			label="Sort: {searchParams.order}"
			icon="arrow-down-up"
			icon2="chevron-down"
			list={order_by}
			bind:value={searchParams.order}
			onchange={(v) => {
				searchParams.page_no = 1;
				page_state.set({ order: v == defaultParams.order ? '' : v });
			}}
		/>
	</div>
</Content>

<Content --content-padding-top="1px">
	{#each reports as report (report.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {report} {update} {searchParams} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No report found
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
