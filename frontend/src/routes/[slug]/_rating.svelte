<script>
	import { module, loading, notification, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Loading from '$lib/loading.svelte';
	import { onMount } from 'svelte';

	let rating = $module.my_rating;
	let post_key = $module.post_key;
	let error = {};

	const set_active = (val) => {
		rating = val;
	};

	const submit = async () => {
		error = {};

		$loading = 'Saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/rating/${post_key}`, {
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
			$module.update_my_rating(rating);
			$module = null;
			$notification = {
				message: 'Rating Saved'
			};
		} else {
			error = resp;
		}
	};

	let _loading = false;
	onMount(async () => {
		if (rating == null) {
			_loading = true;

			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/rating/${post_key}`);
			resp = await resp.json();

			if (resp.status == 200) {
				rating = 0;
				for (const i in resp.ratings) {
					if (resp.ratings[i].user_key == $user.key) {
						rating = resp.ratings[i].rating;
						break;
					}
				}
				$module.update_my_rating(rating);
			}
			_loading = false;
		}
	});
</script>

<section>
	<strong class="ititle"> Add Rating </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div>
		Rating ({rating})
		<div class="block" class:disable={_loading}>
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
			{#if _loading}
				<div class="loading">
					<Loading size="40" />
				</div>
			{/if}
		</div>
	</div>

	<Button on:click={submit}>
		Submit
		<Icon icon="send" />
	</Button>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		padding: var(--sp3);
	}

	.block {
		position: relative;

		display: flex;
		align-items: center;
		overflow: hidden;
	}

	.disable {
		opacity: 0.5;
		pointer-events: none;
	}

	.loading {
		position: absolute;
		inset: 0;

		display: flex;
		justify-content: center;
		align-items: center;
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
</style>
