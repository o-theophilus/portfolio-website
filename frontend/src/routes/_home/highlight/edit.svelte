<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Button, RoundButton } from '$lib/button';
	import { Form } from '$lib/layout';

	let posts = $state([...app.featured]);
	let init = $state([...app.featured]);
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
		posts = [...app.featured];
		init = [...app.featured];
	};

	const submit = async () => {
		error = {};

		loading.open('Updating feature . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/posts/feature`, {
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
			app.featured = resp.posts;
			posts = [...app.featured];
			init = [...app.featured];
			module.value.reset_index();
			notify.open('Feature updated');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Featured Post" error={error.error}>
	{#each posts as x, i (x.key)}
		<div class="post" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<div class="title">
				{x.title}
			</div>

			<div class="btns">
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

	<div class="line">
		<Button icon="save" onclick={submit} disabled={JSON.stringify(posts) === JSON.stringify(init)}>
			Save
		</Button>
		<Button
			icon="history"
			onclick={reset}
			disabled={JSON.stringify(posts) === JSON.stringify(init)}
		>
			Reset
		</Button>
	</div>
</Form>

<style>
	.post {
		display: flex;
		gap: 16px;
		justify-content: space-between;
		align-items: center;

		padding: 8px;
		margin-top: 8px;
		border-radius: 8px;
		background-color: var(--bg1);

		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}

	.title {
		width: 100%;
		font-size: 0.7rem;
	}

	.btns {
		flex-shrink: 0;
	}

	.line {
		margin-top: 16px;
	}
</style>
