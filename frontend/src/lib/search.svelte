<script>
	import { createEventDispatcher } from 'svelte';
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import { RoundButton, Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	let emit = createEventDispatcher();

	export let search = '';
	export let placeholder = 'Search';
	export let non_default = false;
	let _search = `${search}`;

	let set = (url) => {
		if (!non_default) {
			_search = search = '';
			if (url.searchParams.has('search')) {
				_search = search = url.searchParams.get('search');
			}
		}
	};

	const submit = (x) => {
		if (x == 'clear' || search.trim() == '') {
			search = '';
		}
		emit(x);

		if (!non_default) {
			if (_search != search) {
				page_state.set('search', search);
			}
			set(page.url);
		}
	};

	onMount(() => {
		set(page.url);
	});
	$: set(page.url);
</script>

<IG type="text" {placeholder} bind:value={search} no_pad>
	<svelte:fragment slot="right">
		<div class="right">
			{#if search}
				<div class="close">
					<RoundButton
						icon="close"
						extra="hover_red"
						onclick={() => {
							submit('clear');
						}}
					/>
				</div>
			{/if}

			<slot>
				{#if !non_default}
					<Button
						onclick={() => {
							submit('ok');
						}}
						disabled={search == _search}
					>
						<Icon icon="search" />
					</Button>
				{/if}
			</slot>
		</div>
	</svelte:fragment>
</IG>

<style>
	.right {
		display: flex;
		align-items: center;
		margin-right: 6px;
	}
	.close {
		margin-right: var(--sp1);
	}
</style>
