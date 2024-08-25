<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notification, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	let post = $module.post;
	let files = [...post.files];
	let active_photo = files[0] || '/no_photo.png';
	let count = post.content.split('@[file]').length;
	let error = {};

	const order = (dir = true) => {
		error = {};
		const old_i = files.findIndex((x) => x == active_photo);

		if (old_i == -1) {
			return;
		}

		let new_i = old_i - 1;
		if (dir) {
			new_i = old_i + 1;
		}

		if (new_i < 0 || new_i >= files.length) {
			return;
		}

		const temp = files[new_i];
		files[new_i] = files[old_i];
		files[old_i] = temp;
	};

	const remove = () => {
		error = {};

		files = files.filter((x) => x != active_photo);
		active_photo = files[0] || '/no_photo.png';
		emit('active', active_photo);
	};

	export const reset = (data) => {
		error = {};

		post.files = [...data];
		files = [...data];
		if (!files.includes(active_photo)) {
			active_photo = files[0] || '/no_photo.png';
			emit('active', active_photo);
		}
	};

	const submit = async () => {
		error = {};

		$loading = 'Saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/photo/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ files })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			post = resp.post;
			$module.update(post);
			emit('update', post.files);
			reset(post.files);

			$notification = {
				message: 'Order Saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<div class="line">
	{#each files as x, i (x)}
		<img
			animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
			src="{x}/200"
			alt={post.name}
			class:excess={i > count - 1}
			class:active={active_photo == x}
			on:click={() => {
				error = {};
				active_photo = x;
				emit('active', active_photo);
			}}
			role="presentation"
		/>
	{/each}

	{#if count - files.length > 0}
		{#each Array(count - files.length) as _, i (i)}
			<div
				class="empty"
				animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
				on:click={() => {
					if (post.files.length < count) {
						emit('add');
					} else {
						error.error = 'save changes and try again';
					}
				}}
				role="presentation"
			>
				<Icon icon="add" />
			</div>
		{/each}
	{/if}
</div>

<div class="line">
	<BRound
		icon="arrow_back"
		disabled={files.length <= 1 || files[0] == active_photo}
		on:click={() => {
			order(false);
		}}
	/>

	<BRound
		icon="arrow_forward"
		disabled={files.length <= 1 || files[files.length - 1] == active_photo}
		on:click={order}
	/>

	<BRound icon="delete" disabled={files.length == 0} on:click={remove} />
</div>

<br />

<div class="line">
	<Button disabled={JSON.stringify(post.files) == JSON.stringify(files)} on:click={submit}>
		<Icon icon="save" />
		Save
	</Button>

	<Button
		on:click={() => {
			reset(post.files);
		}}
		disabled={JSON.stringify(post.files) == JSON.stringify(files)}
	>
		<Icon icon="history" />
		Reset
	</Button>
</div>

{#if error.error}
	<div class="error">
		{error.error}
	</div>
{/if}

<style>
	.line {
		--size: 50px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);
		flex-wrap: wrap;
		margin-top: var(--sp2);
	}

	img,
	.empty {
		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);
		cursor: pointer;

		outline: 2px solid transparent;
		transition: outline-color var(--trans), transform var(--trans);
	}

	img:hover,
	.empty:hover {
		outline-color: var(--cl1);
	}

	.excess {
		outline-color: var(--cl2);
		opacity: 0.5;
	}

	.active {
		outline-color: var(--cl1);
		transform: scale(1.1);
	}

	.empty {
		display: flex;
		justify-content: center;
		align-items: center;

		background-color: var(--bg2);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
