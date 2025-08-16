<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notify, app, module } from '$lib/store.svelte.js';

	import { Button, RoundButton } from '$lib/button';
	import { slide } from 'svelte/transition';

	let posts = $state([...app.highlight]);
	let init = $state([...app.highlight]);
	let error = $state({});

	const order = (key, down = true) => {
		const index = posts.findIndex((x) => x.key == key);

		if (index == -1) {
			return posts;
		}

		let newIndex = index - 1;
		if (down) {
			newIndex = index + 1;
		}

		if (newIndex < 0 || newIndex >= posts.length) {
			return posts;
		}

		const temp = posts[newIndex];
		posts[newIndex] = posts[index];
		posts[index] = temp;
	};

	const remove = (key) => {
		posts = posts.filter((i) => i.key != key);
	};

	export const reset = () => {
		posts = [...app.highlight];
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
				keys: posts.map((x) => x.key)
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.highlight = resp.posts;
			posts = [...app.highlight];
			init = [...app.highlight];
			module.value.reset_index();
			notify.open('Highlight updated');
		} else {
			error = resp;
		}
	};
</script>

{#each posts as x, i (x.key)}
	<div class="line space" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
		<div class="post_name">
			{x.title}
		</div>

		<div>
			<RoundButton
				icon="chevron-up"
				disabled={i == 0}
				onclick={() => {
					order(x.key, false);
				}}
			/>
			<RoundButton
				icon="chevron-down"
				disabled={i == posts.length - 1}
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
	<Button icon="save" onclick={submit} disabled={JSON.stringify(posts) === JSON.stringify(init)}>
		Save
	</Button>
	<Button icon="history" onclick={reset} disabled={JSON.stringify(posts) === JSON.stringify(init)}>
		Reset
	</Button>
</div>

<style>
	.line {
		margin-top: var(--sp1);
	}

	.post_name {
		font-size: 0.8rem;
	}

	.error {
		margin: 16px 0;
		font-size: 0.8rem;
		color: red;
	}
</style>
