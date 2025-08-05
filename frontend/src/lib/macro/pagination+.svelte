<script>
	import { page_state } from '$lib/store.svelte.js';
	import { Pagination } from '$lib/input';

	let { value = $bindable(), total_page, ondone } = $props();
	let pagination = $state();

	$effect(() => {
		let page_no = page_state.searchParams.page_no;
		if (value != page_no) {
			pagination?.reset(page_no ? page_no : 1);
		}
	});
</script>

{#if total_page > 1}
	<Pagination
		bind:this={pagination}
		bind:value
		{total_page}
		ondone={() => {
			let x = value != 1 ? value : '';
			page_state.set('page_no', x);
			ondone?.(x);
		}}
	></Pagination>
{/if}
