<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notify, app, module } from '$lib/store.svelte.js';

	import { Button, RoundButton } from '$lib/button';
	import { slide } from 'svelte/transition';

	let items = $state([...app.highlight]);
	let init = $state([...app.highlight]);
	let error = $state({});

	const order = (key, down = true) => {
		const index = items.findIndex((x) => x.key == key);

		if (index == -1) {
			return items;
		}

		let newIndex = index - 1;
		if (down) {
			newIndex = index + 1;
		}

		if (newIndex < 0 || newIndex >= items.length) {
			return items;
		}

		const temp = items[newIndex];
		items[newIndex] = items[index];
		items[index] = temp;
	};

	const remove = (key) => {
		items = items.filter((i) => i.key != key);
	};

	export const reset = () => {
		items = [...app.highlight];
		init = [...app.highlight];
	};

	const submit = async () => {
		error = {};

		loading.open('saving . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				keys: items.map((x) => x.key)
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.highlight = resp.items;
			items = [...app.highlight];
			init = [...app.highlight];
			module.value.reset_index();
			notify.open('Highlight updated');
		} else {
			error = resp;
		}
	};
</script>

{#each items as x, i (x.key)}
	<div class="line space" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
		<div class="post_name">
			{x.title}
		</div>

		<div class="buttons">
			<RoundButton
				icon="chevron-up"
				disabled={i == 0}
				onclick={() => {
					order(x.key, false);
				}}
			/>
			<RoundButton
				icon="chevron-down"
				disabled={i == items.length - 1}
				onclick={() => {
					order(x.key);
				}}
			/>
			<RoundButton
				icon="trash-2"
				--button-background-color-hover="red"
				onclick={() => {
					remove(x.key);
				}}
			/>
		</div>
	</div>
{/each}

{#if error.error}
	<div class="error" transition:slide>
		{error.error}
	</div>
{/if}

<div class="line">
	<Button icon="save" onclick={submit} disabled={JSON.stringify(items) === JSON.stringify(init)}>
		Save
	</Button>
	<Button icon="history" onclick={reset} disabled={JSON.stringify(items) === JSON.stringify(init)}>
		Reset
	</Button>
</div>

<style>
	.line {
		margin-top: var(--sp1);
		flex-wrap: nowrap;
	}

	.buttons {
		flex-shrink: 0;
	}

	.post_name {
		width: 100%;
		font-size: 0.8rem;
	}

	.error {
		margin: 16px 0;
		font-size: 0.8rem;
		color: red;
	}
</style>
