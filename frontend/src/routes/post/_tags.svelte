<script>
	import { page } from '$app/stores';

	import { onMount } from 'svelte';
	import { set_state, module, state } from '$lib/store.js';
	import Toggle from '$lib/toggle.svelte';
	import Input from '$lib/input.svelte';
	import BRound from '$lib/button/round.svelte';
	import Button from '$lib/button/button.svelte';
	import Form from '$lib/form.svelte';
	import Tag from '$lib/button/tag.svelte';
	import Spinner from '$lib/loading_spinner.svelte';

	let tags = [];
	let selected = [];
	let _selected = [];
	let multiply = false;
	let _multiply = false;
	let filter = '';

	let selected_string = '';
	let _selected_string = '';

	$: {
		selected_string = selected.sort((a, b) => a - b).join(',');
		selected_string = `${selected_string}${selected.length > 1 && multiply ? ':x' : ''}`;
		_selected_string = _selected.sort((a, b) => a - b).join(',');
		_selected_string = `${_selected_string}${_selected.length > 1 && _multiply ? ':x' : ''}`;
	}

	// TODO: use this compponent
	let loading_tags = true;
	onMount(async () => {
		let pn = 'tags';
		let i = $state.findIndex((x) => x.name == pn);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();
			loading_tags = false;

			if (resp.status == 200) {
				tags = resp.tags;
				$state.push({
					name: pn,
					data: resp.tags
				});
			}
		} else {
			tags = $state[i].data;
			loading_tags = false;
		}

		let params = $page.url.searchParams;
		if (params.has('tag')) {
			let x = params.get('tag');
			if (x.slice(-2) == ':x') {
				x = x.slice(0, -2);
				multiply = true;
				_multiply = true;
			}
			selected = x.split(',');
			_selected = x.split(',');
		}
	});

	const toggle = (x) => {
		if (selected.includes(x)) {
			selected = selected.filter((i) => i != x);
		} else {
			selected.push(x);
			selected = selected;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>All Tags</b>
	</svelte:fragment>

	<div class="input">
		<Input bind:value={filter} type="text" placeholder="Filter" />
		{#if filter}
			<div class="clear">
				<BRound
					icon="close"
					icon_size="8"
					on:click={() => {
						filter = '';
					}}
				/>
			</div>
		{/if}
	</div>

	<br />

	<div class="tags_space">
		{#if loading_tags}
			<div class="spinner">
				<Spinner active />
			</div>
		{/if}
		{#each tags as x}
			{#if x.includes(filter.toLowerCase())}
				<Tag
					active={selected.includes(x)}
					on:click={() => {
						toggle(x);
					}}
				>
					{x}
				</Tag>
			{/if}
		{/each}
	</div>

	<br />

	<div class="row">
		<Toggle
			state_1="any"
			state_2="all"
			active={multiply}
			disabled={selected.length < 2}
			on:click={() => {
				multiply = !multiply;
			}}
		/>

		<div class="row buttons">
			<Button
				disabled={!_selected_string && !selected_string}
				extra="hover_red"
				on:click={() => {
					if (_selected_string) {
						set_state('tag', '');
					}

					selected = [];
					_selected = [];
					multiply = false;
					_multiply = false;
					$module = '';
				}}
			>
				Clear
			</Button>

			<Button
				disabled={_selected_string == selected_string}
				on:click={() => {
					set_state('tag', selected_string);

					_selected = selected;
					_multiply = multiply;
					$module = '';
				}}
			>
				Ok
			</Button>
		</div>
	</div>
</Form>

<style>
	.input {
		position: relative;
	}
	.clear {
		position: absolute;
		top: 0;
		right: var(--sp1);

		display: flex;
		align-items: center;
		height: 100%;
	}

	.tags_space {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		max-height: 200px;
		overflow-y: auto;

		border-radius: var(--sp1);
		padding: var(--sp1);
		border: 2px solid var(--ac4);
	}
	.spinner {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100px;
		width: 100%;
	}

	.row {
		display: flex;
		gap: var(--sp3);
		justify-content: space-between;
		align-items: center;
	}

	.buttons {
		gap: var(--sp0);
	}
</style>
