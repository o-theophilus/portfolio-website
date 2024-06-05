<script>
	import { module, portal, user, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	export let ratings;
	export let post_key;
	let rating = 0;
	let error = {};

	for (const i in ratings) {
		if (ratings[i].user_key == $user.key) {
			rating = ratings[i].rating;
			break;
		}
	}

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
			$portal = {
				for: 'rating',
				data: resp.ratings
			};

			$module = '';
		} else {
			error = resp;
		}
	};
</script>

<section>
	<strong class="ititle"> Add Rating </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<div>
		Rating ({rating})
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
		background-color: var(--ac3);
	}

	.b0:hover,
	.b0.active {
		background-color: var(--ac1);
	}

	button {
		width: 20px;
		height: 50px;

		border: none;
		background-color: var(--ac4);

		cursor: pointer;
	}
</style>
