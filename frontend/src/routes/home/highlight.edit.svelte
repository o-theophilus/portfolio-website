<script>
	import { loading, portal, module, settings } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	let posts = [...$settings.highlight];
	let init_order = [...posts];
	let error = {};

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

	const remove = async (key) => {
		posts = posts.filter((i) => i.key != key);
	};

	const reset = async () => {
		console.log(1);
		posts = [...$settings.highlight];
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
			$module = null;
		} else {
			error = resp;
		}
	};
</script>

<div class="comp">
	<strong class="big"> Edit Highlights </strong>
	{#each posts as x, i}
		<div class="line">
			{x.title}

			<Button
				class="tiny"
				disabled={i == 0}
				on:click={() => {
					move_down(x.key, false);
				}}
			>
				up
			</Button>
			<Button
				class="tiny"
				disabled={i == posts.length - 1}
				on:click={() => {
					move_down(x.key);
				}}
			>
				dn
			</Button>
			<Button
				class="tiny"
				extra="hover_red"
				on:click={() => {
					remove(x.key);
				}}
			>
				Remove
			</Button>
		</div>
	{/each}

	<Button class="tiny" disabled={init_order == posts} on:click={submit}>Submit</Button>
	<Button class="tiny" disabled={init_order == posts} on:click={reset}>Reset</Button>

	{#if error.error}
		<br />
		<span class="error">
			{error.error}
		</span>
		<br />
	{/if}
</div>

<style>
	.comp {
		padding: var(--sp3);
	}
	/* .row {
		display: flex;
		justify-content: center;
		gap: var(--sp1);
		flex-wrap: wrap;
		margin-top: var(--sp2);
	} */
</style>
