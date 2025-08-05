<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let rating = 0;
	let error = {};
	for (const x of module.value.post.ratings) {
		if (x.user_key == app.user.key) {
			rating = x.rating;
			break;
		}
	}

	const validate = () => {
		error = {};

		if (!rating) {
			error.error = 'cannot rate 0';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Saving . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/rating/${module.value.post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ rating })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.post);
			module.value.set_rating(resp.post);
			module.close();
			notify.open('Rating Saved');
		} else {
			error = resp;
		}
	};

	const set_active = (val) => {
		rating = val;
	};
</script>

<section>
	<strong class="ititle"> Add Rating </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div class="label">
		Rating ({rating})
	</div>
	<div class="block">
		<div class="block red">
			{#each Array(5) as _, i}
				{@const j = -5 + i}
				<button class:active={j == rating} onclick={() => set_active(j)}>ooooo</button>
			{/each}
		</div>
		<button class:active={0 == rating} class="b0" onclick={() => set_active(0)}>ooooo</button>
		<div class="block green">
			{#each Array(5) as _, i}
				{@const j = 5 - i}
				<button class:active={j == rating} onclick={() => set_active(j)}>ooooo</button>
			{/each}
		</div>
	</div>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</section>

<style>
	section {
		padding: var(--sp3);
	}

	.block {
		position: relative;

		display: flex;
		align-items: center;
		overflow: hidden;
	}

	.green {
		flex-direction: row-reverse;
		border-radius: 0 var(--sp1) var(--sp1) 0;
	}
	.red {
		border-radius: var(--sp1) 0 0 var(--sp1);
		overflow: hidden;
	}

	.red button.active ~ button,
	.red button:hover ~ button {
		background-color: coral;
	}
	.red button.active,
	.red button:hover {
		background-color: var(--cl2) !important;
	}

	.green button.active ~ button,
	.green button:hover ~ button {
		background-color: lime;
	}
	.green button.active,
	.green button:hover {
		background-color: var(--cl3) !important;
	}

	.b0 {
		border-radius: var(--sp1);
		width: 5px;
		height: 70px;
		background-color: var(--bg2);
	}

	.b0:hover,
	.b0.active {
		background-color: var(--ft1);
	}

	button {
		width: 20px;
		height: 50px;

		border: none;
		background-color: var(--bg2);

		cursor: pointer;
	}

	.error {
		margin: var(--sp2) 0;
	}
	.label {
		margin-top: var(--sp2);
		font-size: 0.8rem;
	}
</style>
