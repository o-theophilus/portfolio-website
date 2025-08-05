<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store_old.js';

	import BRound from '$lib/button_old/round.svelte';
	import Content from '$lib/content.svelte';

	let text = '';
	let set = (url) => {
		let _s = '';
		let _t = '';
		let multiply = false;
		if (url.searchParams.has('search')) {
			_s = url.searchParams.get('search');
			_s = ` for [${_s}]`;
		}
		if (url.searchParams.has('tag')) {
			_t = url.searchParams.get('tag');
			multiply = _t.substring(_t.length - 2, _t.length) == ':x';
			if (multiply) {
				_t = _t.substring(0, _t.length - 2);
			}
			_t = _t.split(',');
			_t = ` with ${_t.length > 1 ? (multiply ? 'all' : 'any') : ''} tag${
				_t.length > 1 && multiply ? 's' : ''
			} [${_t.join(', ')}]`;
		}

		text = `${_s || _t ? 'Showing result' : ''}${_s}${_t}`;
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);
</script>

{#if text}
	<div class="filter">
		<span>
			{text}
		</span>

		<BRound
			icon="close"
			extra="hover_red"
			on:click={() => {
				set_state('search', '');
				set_state('tag', '');
			}}
		/>
	</div>
{/if}

<style>
	.filter {
		display: flex;
		gap: var(--sp2);
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp2);

		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: color-mix(in srgb, var(--cl1), transparent 90%);
		color: var(--ft1);
		font-size: 0.8rem;
	}
</style>
