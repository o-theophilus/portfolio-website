<script>
	import { module } from '$lib/store.js';

	import Marked from '$lib/comp/marked.svelte';
	import Button from '$lib/comp/button.svelte';
	import Add_Comment from '$lib/module/add_comment.svelte';

	export let post = [];
	export let key;

	let saturation = Math.floor(Math.random() * (360 + 1));
</script>

{#each post.comments as c}
	{#if c.comment_key == key}
		<div class="comment">
			<div class="top">
				<div class="left">
					<div
						class="img"
						class:light={saturation > 29 && saturation < 189}
						style:--saturation={saturation}
					>
						{c.name[0]}
					</div>
					<div class="name">{c.name}</div>
				</div>
				<div class="date">{c.created_at.split('T')[0]}</div>
			</div>
			<div>
				<Marked md={c.comment} />
				<Button
					name="Add comment"
					class="secondary"
					on:click={() => {
						$module = {
							module: Add_Comment,
							post,
							comment_key: c.key
						};
					}}
				/>
			</div>
			<slot key={c.key} />
		</div>
	{/if}
{/each}

<style>
	.comment {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		padding: var(--gap2);
		padding-right: 0;

		border: 1px solid var(--mid_color);
		border-right-width: 0;

		border-top-left-radius: var(--gap0);
		border-bottom-left-radius: var(--gap0);
	}

	.top,
	.left {
		display: flex;
		align-items: center;
		gap: var(--gap2);
	}
	.top {
		justify-content: space-between;
	}

	.img {
		--size: 50px;

		background-color: hsl(var(--saturation), 100%, 50%);
		border-radius: 50%;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		display: flex;
		align-items: center;
		justify-content: center;

		text-transform: capitalize;
		font-size: larger;
		font-weight: bold;

		color: var(--light_color);
	}
	.light {
		color: var(--dark_color);
	}
	.date {
		color: var(--mid_color);
	}
</style>
