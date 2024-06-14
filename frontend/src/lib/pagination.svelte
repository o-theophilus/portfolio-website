<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';

	let _value, value, width;
	export let total_page = 1;

	const normalize = (x) => {
		if (x < 1) {
			x = 1;
		} else if (x > total_page) {
			x = total_page;
		}
		return x;
	};

	const submit = (x) => {
		x = normalize(x);
		_value = value = x;
		set_state('page_no', x != 1 ? x : '');
	};

	let set = (url) => {
		_value = value = 1;
		if (url.searchParams.has('page_no')) {
			_value = value = normalize(url.searchParams.get('page_no'));
		}
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);
</script>

{#if total_page > 1}
	<hr />

	<section>
		{#if _value > 1}
			<button
				on:click={() => {
					submit(_value - 1);
				}}
			>
				<Icon icon="arrow_back" />
			</button>
		{/if}

		<div class="input">
			<input
				style:width="calc({width}px + 4px)"
				type="text"
				oninput="this.value = this.value.replace(/[^0-9]/g, '')"
				bind:value
				on:keypress={(e) => {
					if (e.key == 'Enter') {
						submit(value);
					}
				}}
			/>
			<div class="total">
				/ {total_page}
			</div>
		</div>

		<div class="width_helper" bind:clientWidth={width}>
			<span>
				{#if value}
					{value}
				{:else}
					0
				{/if}
			</span>
			/ {total_page}
		</div>

		{#if value != _value}
			<button
				on:click={() => {
					submit(value);
				}}
			>
				<Icon icon="keyboard_double_arrow_right" />
			</button>
		{/if}

		{#if _value < total_page}
			<button
				on:click={() => {
					submit(parseInt(_value) + 1);
				}}
			>
				<Icon icon="arrow_forward" />
			</button>
		{/if}
	</section>
{/if}

<style>
	section {
		--size: var(--sp3);
		--height: 48px;

		display: flex;
		gap: var(--sp0);

		width: fit-content;
		margin: var(--sp2) auto;
		border-radius: var(--sp0);

		outline: 2px solid transparent;
		background-color: var(--input);

		transition: outline-color var(--trans);
	}
	section:hover,
	section:has(input:focus) {
		outline-color: var(--ft1);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	input {
		padding: var(--size);
		height: var(--height);
		border: none;

		color: var(--ft1);
		background-color: transparent;
	}

	.total {
		position: absolute;
		right: var(--size);
		pointer-events: none;
	}

	.width_helper {
		position: absolute;
		visibility: hidden;
		padding: var(--size);
		display: inline-block;
	}

	button {
		display: flex;
		justify-content: center;
		align-items: center;

		height: var(--height);
		aspect-ratio: 1/1;

		border-radius: var(--sp0);
		background-color: var(--button);
		color: var(--ft2_b);
		border: none;
		cursor: pointer;
		font-weight: 700;

		transition: color var(--trans), background-color var(--trans);
	}

	button:hover {
		background-color: var(--cl1);
		color: var(--ft1_b);
	}
</style>
