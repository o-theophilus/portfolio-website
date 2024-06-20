<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notification, settings } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';

	let posts = [...$settings.highlight];
	let init_order = [...$settings.highlight];
	let error = {};

	$: not_changed =
		`${posts.map((obj) => JSON.stringify(obj))}` ==
		`${init_order.map((obj) => JSON.stringify(obj))}`;

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
		posts = [...$settings.highlight];
		init_order = [...$settings.highlight];
	};

	const submit = async () => {
		error = {};

		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				keys: posts.map((x) => x.key)
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$settings.highlight = resp.posts;

			$notification = {
				status: 200,
				message: 'Highlight updated'
			};
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

		<BRound
			icon="arrow_upward"
			disabled={i == 0}
			on:click={() => {
				move_down(x.key, false);
			}}
		/>
		<BRound
			icon="arrow_downward"
			disabled={i == posts.length - 1}
			on:click={() => {
				move_down(x.key);
			}}
		/>
		<BRound
			icon="delete"
			extra="hover_red"
			on:click={() => {
				remove(x.key);
			}}
		/>
	</div>
{/each}

<div class="line">
	<Button class="tiny" disabled={not_changed} on:click={submit}>
		<Icon icon="save" />
		Save
	</Button>
	<Button class="tiny" disabled={not_changed} on:click={reset}>
		<Icon icon="history" />
		Reset
	</Button>
</div>

{#if error.error}
	<span class="error">
		{error.error}
	</span>
{/if}

<style>
	.line {
		display: flex;
		gap: var(--sp1);
		margin-top: var(--sp2);
	}

	.post_name {
		width: 100%;
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
