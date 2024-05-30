<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

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
	<div class="center">
		<hr />

		<section>
			{#if _value > 1}
				<button
					on:click={() => {
						submit(_value - 1);
					}}
				>
					&lt;
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
					&gt;&gt;
				</button>
			{/if}

			{#if _value < total_page}
				<button
					on:click={() => {
						submit(parseInt(_value) + 1);
					}}
				>
					&gt;
				</button>
			{/if}
		</section>
	</div>
{/if}

<style>
	.center {
		width: min(100%, 1200px);
		margin: 0 auto;
		padding: 0 var(--sp2);
	}

	hr {
		border-color: var(--ac3);
	}

	section {
		--size: var(--sp1);
		--height: 40px;

		display: flex;

		width: fit-content;
		margin: auto;
		border-radius: var(--sp0);
		overflow: hidden;

		color: var(--ac3);
		outline: 2px solid var(--ac4);
	}
	section:hover {
		outline-color: var(--ac3);
	}
	section:has(input:focus) {
		outline-color: var(--ac1);
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

		color: var(--ac1);
		background-color: var(--ac5);
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
		aspect-ratio: 1/1;
		height: var(--height);

		background-color: var(--ac6);
		color: var(--ac2);
		border: none;
		cursor: pointer;
		font-weight: 700;
	}

	button:hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
</style>
