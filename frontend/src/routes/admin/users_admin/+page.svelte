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
	import One from '../users/one.svelte';

	let { data } = $props();
	let users = $derived(data.users);
	let total_page = $derived(data.total_page);
	let { access } = data;

	let { order_by } = data;
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

<Log entity_type={'page'} />
<Meta title="Admin" description="Users with elevated Access" />

<Content --content-height="auto">
	<div class="page_title">
		Admin{users.length > 1 ? 's' : ''}
	</div>

	<br />
	<div class="line nowrap">
		<Dropdown
			icon2="chevron-down"
			list={Object.keys(access)}
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
			list={access[searchParams.entity_type]}
			bind:value={searchParams.action}
			onchange={(v) => {
				searchParams.page_no = 1;
				page_state.set({ action: v == defaultParams.action ? '' : v });
			}}
			--select-width="100%"
		/>
	</div>

	<Search
		bind:value={searchParams.search}
		ondone={(v) => {
			searchParams.page_no = 1;
			page_state.set({ search: v });
		}}
	></Search>

	<Dropdown
		--select-height="10"
		--select-padding-x="0"
		--select-font-size="0.8rem"
		--select-background-color="transparent"
		--select-background-color-hover="transparent"
		--select-color-hover="var(--ft1)"
		--select-outline-color="transparent"
		list={order_by}
		icon="arrow-down-narrow-wide"
		icon2="chevron-down"
		bind:value={searchParams.order}
		onchange={(v) => {
			searchParams.page_no = 1;
			page_state.set({ order: v == defaultParams.order ? '' : v });
		}}
	/>
</Content>

<Content --content-padding-top="1px">
	{#each users as user (user.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {user} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No user found
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
