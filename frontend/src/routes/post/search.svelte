<script>
	import { createEventDispatcher } from 'svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

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
	<div class="input">
		<div class="float svg">
			<SVG icon="search" size="15" />
		</div>

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

		<div class="float clear">
			<!-- {#if search} -->
				<BRound
					icon="close"
					icon_size="8"
					extra=hover_red
					on:click={() => {
						submit('clear');
					}}
				/>
			<!-- {/if} -->
		</div>
	</div>

	{#if !non_default}
		<button
			on:click={() => {
				submit('ok');
			}}
			disabled={search == _search}
			>Search
		</button>
	{/if}
</div>

<style>
	.comp {
		margin-top: var(--sp3);
		display: flex;
	}

	.input {
		position: relative;

		display: flex;
		align-items: center;
		width: 100%;
		/* height: 40px; */

		fill: var(--ac3);

		border-radius: var(--sp0) 0 0 var(--sp0);
		outline: 2px solid var(--ac4);
		/* outline-offset: -2px; */
		background-color: var(--ac5);
	}

	input {
		width: 100%;
		height: 100%;
		/* padding: var(--sp1); */
		/* padding-left: var(--sp5); */
		padding-left: var(--sp2);
		border: none;

		color: var(--ac1);
		background-color: transparent;
	}

	input:hover {
		outline-color: var(--ac3);
	}
	input:focus {
		outline-color: var(--ac1);
	}
	.non_default {
		border-radius: var(--sp0);
	}

	.show_close {
		padding-right: var(--sp5);
	}

	.float {
		position: absolute;
		top: 0;
		display: flex;
		align-items: center;
		height: 100%;
	}
	.clear {
		right: var(--sp1);
	}
	.svg {
		left: var(--sp2);
	}

	button {
		padding: calc(var(--sp1) + 2px) var(--sp2);
		border: none;
		border-radius: 0 var(--sp0) var(--sp0) 0;
		font-weight: 700;
		cursor: pointer;
		background-color: var(--cl1);
		color: var(--ac6_);
	}

	button:hover:not(:disabled) {
		background-color: var(--cl1_b);
	}

	button:disabled {
		background-color: var(--ac5);
		color: var(--ac2);
		cursor: unset;
		opacity: 0.4;
	}
</style>
