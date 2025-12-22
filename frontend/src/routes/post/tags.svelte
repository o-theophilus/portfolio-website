<script>
	import { slide } from 'svelte/transition';
	import { onMount } from 'svelte';
	import { app } from '$lib/store.svelte.js';

	import { Toggle, Button, RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { IG } from '$lib/input';

	let { value = $bindable(), ondone } = $props();

	let selected = $state([]);
	let multiply = $state(false);
	let filter = $state('');
	let loading = $state(true);
	let open = $state(false);

	let _selected = $state([]);
	let _multiply = $state(false);

	onMount(async () => {
		if (!app.tags) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.tags = resp.tags;
			}
		}

		if (value.endsWith(':all')) {
			multiply = true;
			_multiply = multiply;
			value = value.slice(0, -4);
		}

		selected = value.split(',').filter(Boolean);
		_selected = [...selected];
		loading = false;
	});

	const submit = () => {
		let temp = selected.join(',');
		temp = selected.length > 1 && multiply ? `${temp}:all` : temp;
		ondone(temp);

		_selected = [...selected];
		_multiply = multiply;
	};

	export const clear = () => {
		multiply = false;
		selected = [];
		filter = '';
	};

	const _clear = () => {
		clear();
		if (_selected.length) submit();
		open = false;
	};

	const ok = () => {
		filter = '';
		submit();
		open = false;
	};
</script>

<div class="filter">
	<Button
		icon="list-filter"
		--button-padding-x="0"
		--button-width="48px"
		--button-height="48px"
		onclick={() => {
			open = !open;
			filter = '';
		}}
		disabled={loading}
	></Button>

	{#if open}
		<div class="popup" transition:slide>
			<IG type="text" placeholder="filter" bind:value={filter} no_pad>
				{#snippet right()}
					{#if filter}
						<div class="close">
							<RoundButton
								--button-background-color-hover="red"
								icon="x"
								onclick={() => (filter = '')}
							></RoundButton>
						</div>
					{/if}
				{/snippet}
			</IG>

			<div class="tags">
				{#if app.tags?.length}
					{#each app.tags as x}
						{#if x.toLowerCase().includes(filter.toLowerCase())}
							<button
								class="custom-checkbox"
								onclick={() => {
									if (selected.includes(x)) {
										selected = selected.filter((y) => y != x);
									} else {
										selected.push(x);
									}
								}}
							>
								<div class="checkbox" class:active={selected.includes(x)}>
									<div class="icon">
										<Icon icon="check"></Icon>
									</div>
								</div>
								{x}
							</button>
						{/if}
					{/each}
				{/if}
			</div>

			<div class="multiply">
				<Toggle
					active={multiply}
					state_1="any"
					state_2="all"
					onclick={() => (multiply = !multiply)}
					disabled={selected.length < 2}
				></Toggle>
			</div>

			<div class="buttons">
				<Button
					--button-background-color-hover="red"
					--button-height="32px"
					icon="x"
					onclick={_clear}
					disabled={selected.length == 0 && _selected.length == 0}
				></Button>
				<div class="wide">
					<Button
						--button-width="100%"
						--button-height="32px"
						--button-font-size="0.8rem"
						icon="check"
						onclick={ok}
						disabled={JSON.stringify([...selected].sort()) ==
							JSON.stringify([..._selected].sort()) && multiply == _multiply}
					>
						submit
					</Button>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.filter {
		position: relative;
	}

	.popup {
		z-index: 1;
		position: absolute;
		top: 52px;
		right: 0;
		width: 200px;
		height: 308px;

		display: flex;
		flex-direction: column;

		padding: 0 8px;

		background-color: var(--bg1);
		border-radius: var(--sp0);
		outline: 2px solid var(--bg2);
	}

	.close {
		margin-right: 8px;
	}

	.tags {
		height: 100%;
		padding: 8px;
		overflow: auto;

		outline: 2px solid var(--bg2);
		outline-offset: -2px;
	}

	.custom-checkbox {
		all: unset;

		display: flex;
		align-items: center;
		gap: 16px;

		width: 100%;
		margin: 4px 0;

		font-size: 0.8rem;
		line-height: 100%;
	}

	.checkbox {
		--size: 20px;
		position: relative;

		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: 4px;
		outline: 2px solid var(--input);
		outline-offset: -2px;

		background-color: var(--input);
		cursor: pointer;

		transition: background-color var(--trans);
	}

	.checkbox:hover {
		outline-color: var(--ft1);
	}
	.active {
		background-color: var(--cl1);
	}

	.icon {
		position: absolute;
		inset: 0;

		display: flex;
		align-items: center;
		justify-content: center;
		color: transparent;

		transition: color var(--trans);
	}
	.active .icon {
		color: white;
	}

	.multiply {
		margin: 8px 0;
	}
	.buttons {
		display: flex;
		gap: 8px;

		margin-bottom: 8px;
	}
	.wide {
		width: 100%;
	}
</style>
