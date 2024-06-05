<script>
	import { createEventDispatcher } from 'svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let emit = createEventDispatcher();

	export let non_default = false;
	export let placeholder = 'Search';
	export let search = '';
	let _search = `${search}`;

	let set = (url) => {
		if (!non_default) {
			_search = search = '';
			if (url.searchParams.has('search')) {
				_search = search = url.searchParams.get('search');
			}
		}
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);

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
</script>

<div class="comp">
	<input
		class:non_default
		class:show_close={search != ''}
		type="text"
		{placeholder}
		bind:value={search}
		on:keypress={(e) => {
			if (e.key == 'Enter') {
				submit('ok');
			}
		}}
	/>

	<div class="clear">
		{#if search}
			<BRound
				icon="close"
				extra="hover_red"
				on:click={() => {
					submit('clear');
				}}
			/>
		{/if}
	</div>

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
</div>

<style>
	.comp {
		display: flex;
		align-items: center;
		width: 100%;

		padding: var(--sp0);

		border-radius: var(--sp0);
		outline: 2px solid transparent;
		background-color: var(--ac5);

		transition: outline-color var(--trans);
	}

	input {
		width: 100%;
		height: 100%;
		padding: 0 var(--sp2);
		border: none;

		color: var(--ac1);
		background-color: transparent;
	}

	.comp:hover {
		outline-color: var(--ac1);
	}
	.comp:has(input:focus) {
		outline-color: var(--ac1);
	}
	.non_default {
		border-radius: var(--sp0);
	}

	.show_close {
		padding-right: var(--sp4);
	}

	.clear {
		padding-right: var(--sp1);
	}
</style>
