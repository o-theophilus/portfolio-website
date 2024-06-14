<script>
	import { createEventDispatcher } from 'svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();

	export let search = '';
	let _search = `${search}`;
	export let placeholder = 'Search';
	export let non_default = false;

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
				set_state('search', search);
			}
			set($page.url);
		}
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);
</script>

<IG type="text" {placeholder} bind:value={search} no_pad>
	<svelte:fragment slot="right">
		<div class="right">
			{#if search}
				<div class="close">
					<BRound
						icon="close"
						extra="hover_red"
						on:click={() => {
							submit('clear');
						}}
					/>
				</div>
			{/if}

			<slot>
				{#if !non_default}
					<Button
						on:click={() => {
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
	}
	.close {
		margin-right: var(--sp1);
	}
</style>
