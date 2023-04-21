<script>
	import { api_url, module, tick, _user, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let post;
	let rating = 0;
	let error = '';

	for (const i in post.ratings) {
		if (post.ratings[i].user_key == $_user.key) {
			rating = post.ratings[i].rating;
			break;
		}
	}

	const set_active = (val) => {
		rating = val;
	};

	const submit = async () => {
		error = '';
		$loading = 'Saving . . .';
		const resp = await fetch(`${api_url}/${post.type}/rating/${post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ rating })
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if ([401, 102].includes(data.status)) {
				error = data.message;
			} else if (data.status == 200) {
				tick(data.data.post);

				$module = '';
			} else {
				throw new Error('something went wrong');
			}
		}
	};
</script>

<section>
	<strong class="big"> Add Rating </strong>
	{#if error}
		<span class="error">
			{error}
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

	<Button
		on:click={() => {
			submit();
		}}
	>
		Submit
	</Button>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		padding: var(--gap3);
	}

	.block {
		display: flex;
		align-items: center;
		overflow: hidden;
	}
	.green {
		flex-direction: row-reverse;
		border-radius: 0 var(--gap1) var(--gap1) 0;
	}
	.red {
		border-radius: var(--gap1) 0 0 var(--gap1);
		overflow: hidden;
	}

	.red button.active ~ button,
	.red button:hover ~ button {
		background-color: coral;
	}
	.red button.active,
	.red button:hover {
		background-color: var(--color2) !important;
	}

	.green button.active ~ button,
	.green button:hover ~ button {
		background-color: lime;
	}
	.green button.active,
	.green button:hover {
		background-color: var(--color3) !important;
	}

	.b0 {
		border-radius: var(--gap1);
		width: 5px;
		height: 70px;
		background-color: var(--accent3);
	}

	.b0:hover,
	.b0.active {
		background-color: var(--accent1);
	}

	button {
		width: 20px;
		height: 50px;

		border: none;
		background-color: var(--accent4);

		cursor: pointer;
	}
</style>
