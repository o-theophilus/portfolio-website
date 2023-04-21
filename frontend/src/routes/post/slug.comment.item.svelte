<script>
	import { module, _user, api_url, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Marked from '$lib/marked.svelte';
	import Button from '$lib/button.svelte';
	import Add_Comment from './slug.comment__add__.svelte';
	import Comment from './slug.comment.item.svelte';

	export let post = {};
	export let comment = {};

	const validate = async (vote) => {
		if (comment.upvote.includes($_user.key)) {
			comment.upvote = comment.upvote.filter((e) => e != $_user.key);
		} else if (comment.downvote.includes($_user.key)) {
			comment.downvote = comment.downvote.filter((e) => e != $_user.key);
		}

		if (vote == 'up') {
			comment.upvote.push($_user.key);
		} else if (vote == 'down') {
			comment.downvote.push($_user.key);
		} else {
			return;
		}
		comment = comment;

		submit(vote);
	};

	const submit = async (vote) => {
		const resp = await fetch(`${api_url}/comment/vote/${comment.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ vote })
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 201) {
				error = data.message;
			} else if (data.status == 200) {
				for (const i in post.comments) {
					if (post.comments[i]['key'] == data.data.comment['key']) {
						post.comments[i] = data.data.comment;
						break;
					}
				}

				tick(post);
			} else {
				error.form = data.message;
			}
		}
	};

	let saturation = Math.floor(Math.random() * (360 + 1));
</script>

<div class="comment">
	<div class="top">
		<div class="left">
			<div
				class="img"
				class:light={saturation > 29 && saturation < 189}
				style:--saturation={saturation}
			>
				{comment.user_name[0]}
			</div>
			<div class="name">{comment.user_name}</div>
		</div>
		<div class="date">{comment.created_at.split('T')[0]}</div>
	</div>
	<div>
		<Marked md={comment.comment} />
		{#if $_user.login}
			<Button
				name="Reply"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						owner: comment.key,
						post
					};
				}}
			/> |
			<Button
				name="upvote ({comment.upvote.length})"
				class="secondary"
				on:click={() => {
					validate('up');
				}}
			/> |
			<Button
				name="downvote ({comment.downvote.length})"
				class="secondary"
				on:click={() => {
					validate('down');
				}}
			/>
		{/if}
	</div>
	{#each post.comments as c}
		{#if c.path[c.path.length - 1] == comment.key}
			<Comment {post} comment={c} />
		{/if}
	{/each}
</div>

<style>
	.comment {
		display: flex;
		flex-direction: column;

		padding: var(--gap2);
		padding-right: 0;
		padding-bottom: 0;

		border: 2px solid var(--accent4);
		border-right-width: 0;
		border-bottom-width: 0;

		border-top-left-radius: var(--gap0);
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
		--size: 40px;

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

		color: var(--accent5_);
	}
	.light {
		color: var(--accent1_);
	}
	.date {
		color: var(--accent3);
	}
</style>
