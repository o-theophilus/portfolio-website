<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { Card, Doughnut, Summary } from '$lib/dashboard';
	import { Dropdown } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import { page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	let { data } = $props();
	let { filters } = data;
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
<Meta title="Admin Dashboard" />

<Content>
	<div class="page_title">Admin Dashboard</div>

	<Dropdown
		--select-height="32px"
		--select-padding-x="8px"
		--select-font-size="0.8rem"
		label="Interval: {searchParams.interval}"
		icon="list-filter"
		icon2="chevron-down"
		list={filters}
		bind:value={searchParams.interval}
		onchange={(v) => {
			page_state.set({ interval: v == defaultParams.interval ? '' : v });
		}}
	/>

	<div class="container">
		<div class="four margin">
			<Card>
				<Summary
					title="New Users {searchParams.interval}"
					data={page.data.new_users}
					icon="User"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="New Users {searchParams.interval}"
					data={page.data.new_users}
					icon="User"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="New Users {searchParams.interval}"
					data={page.data.new_users}
					icon="User"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="New Users {searchParams.interval}"
					data={page.data.new_users}
					icon="User"
					interval={searchParams.interval}
				></Summary>
			</Card>
		</div>

		<div class="margin">
			<Card title="Post Status">
				<Doughnut data={page.data.post_summary}></Doughnut>
			</Card>
		</div>

		<br />

		<Card title="Activity Feed">
			Display: Columns
			<br />
			<br />
			New order placed | time
			<br />
			Product updated | time
			<br />
			Customer registered | time
		</Card>
	</div>
</Content>

<style>
	.container {
		container-type: inline-size;
	}

	.four {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(2, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(4, 1fr);
			}
		}
	}

	.margin {
		margin-top: 16px;
	}
</style>
