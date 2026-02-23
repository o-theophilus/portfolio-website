<script>
	import { Button, RoundButton, Switch } from '$lib/button';
	import { Checkbox, Input } from '$lib/input';
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';

	let { value = $bindable(), ondone } = $props();

	let selected = $state([]);
	let multiply = $state(false);
	let filter = $state('');

	let _selected = $state([]);
	let _multiply = $state(false);

	let loading = $state(false);
	onMount(async () => {
		if (!app.tags) {
			loading = true;
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
			resp = await resp.json();
			loading = false;

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
		can_close = false;
	};

	const ok = () => {
		filter = '';
		submit();
		open = false;
		can_close = false;
	};

	let menu = $state();
	let open = $state(false);
	let can_close = $state(false);
</script>

<svelte:window
	onclick={(e) => {
		if (menu && menu.contains(e.target)) return;
		if (open && !can_close) open = false;
		can_close = false;
	}}
/>

<div class="filter">
	<Button
		icon="list-filter"
		--button-padding-x="0"
		--button-width="48px"
		--button-height="48px"
		onclick={() => {
			open = !open;
			can_close = true;
			filter = '';
			selected = [..._selected];
			multiply = _multiply;
		}}
		disabled={loading}
	></Button>

	{#if open}
		<div class="popup" transition:slide bind:this={menu}>
			<div class="search">
				<Input placeholder="filter" bind:value={filter}>
					{#snippet right()}
						{#if filter}
							<div class="clear">
								<RoundButton
									--button-background-color-hover="red"
									icon="x"
									onclick={() => (filter = '')}
								></RoundButton>
							</div>
						{/if}
					{/snippet}
				</Input>
			</div>

			<div class="tags">
				{#if app.tags.length}
					{#each app.tags as x}
						{#if x.toLowerCase().includes(filter.toLowerCase())}
							<Checkbox
								value={selected.includes(x)}
								onclick={() => {
									if (selected.includes(x)) {
										selected = selected.filter((y) => y != x);
									} else {
										selected.push(x);
									}
								}}
								label={x}
							></Checkbox>
						{/if}
					{/each}
				{/if}
			</div>

			<div class="multiply">
				<Switch
					--toggle-height="21px"
					--toggle-font-size="0.8rem"
					--toggle-padding-x="8px"
					list={['any', 'all']}
					value={!multiply ? 'any' : 'all'}
					onclick={() => {
						multiply = !multiply;
					}}
					disabled={selected.length < 2}
				/>
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

		background-color: var(--bg);
		border-radius: 4px;
		outline: 2px solid var(--bg1);
	}

	.search {
		margin: 8px 0;
	}

	.clear {
		margin-right: 8px;
	}

	.tags {
		height: 100%;
		padding: 8px;
		overflow: auto;

		outline: 2px solid var(--bg1);
		outline-offset: -2px;
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
