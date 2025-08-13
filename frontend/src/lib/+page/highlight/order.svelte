<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notify, app, module } from '$lib/store.svelte.js';

	import { Button, RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';

	let posts = $state([...app.highlight]);
	let init = $state([...app.highlight]);
	let error = $state({});

	const move_down = (key, dir = true) => {
		const index = posts.findIndex((x) => x.key == key);

		if (index == -1) {
			return posts;
		}

		let newIndex = index - 1;
		if (dir) {
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
			module.value.update();
			notify.open('Highlight updated');
		} else {
			error = resp;
		}
	};
</script>

{#each posts as x, i (x.key)}
	<div class="line" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
		<div class="post_name">
			{x.title}
		</div>

		<RoundButton
			icon="arrow_upward"
			disabled={i == 0}
			onclick={() => {
				move_down(x.key, false);
			}}
		/>
		<RoundButton
			icon="arrow_downward"
			disabled={i == posts.length - 1}
			onclick={() => {
				move_down(x.key);
			}}
		/>
		<RoundButton
			icon="delete"
			extra="hover_red"
			onclick={() => {
				remove(x.key);
			}}
		/>
	</div>
{/each}

{#if error.error}
	<div class="error">
		{error.error}
	</div>
{/if}

<div class="line">
	<Button onclick={submit} disabled={JSON.stringify(posts) === JSON.stringify(init)}>
		<Icon icon="save" />
		Save
	</Button>
	<Button onclick={reset} disabled={JSON.stringify(posts) === JSON.stringify(init)}>
		<Icon icon="history" />
		Reset
	</Button>
</div>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
		margin-top: var(--sp1);
	}

	.post_name {
		font-size: 0.8rem;
		width: 100%;
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
