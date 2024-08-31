<script>
	import { module, loading, notify, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let rating = 0;
	let error = {};
	for (const x of $module.post.ratings) {
		if (x.user_key == $user.key) {
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

		$loading = 'Saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/rating/${$module.post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ rating })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module.update(resp.post);
			$module.set_rating(resp.post);
			$module = null;
			$notify.add('Rating Saved');
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
				<button
					class:active={j == rating}
					on:click={() => {
						set_active(j);
					}}
				/>
			{/each}
		</div>
		<button
			class:active={0 == rating}
			class="b0"
			on:click={() => {
				set_active(0);
			}}
		/>
		<div class="block green">
			{#each Array(5) as _, i}
				{@const j = 5 - i}
				<button
					class:active={j == rating}
					on:click={() => {
						set_active(j);
					}}
				/>
			{/each}
		</div>
	</div>

	<Button on:click={validate}>
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
