<script>
	import { module, _user, api_url, portal, timeAgo } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { onMount } from 'svelte';

	import Marked from '$lib/marked.svelte';
	import Button from '$lib/button.svelte';
	import Add_Comment from './comment__add__.svelte';
	import Comment from './comment.item.svelte';
	import Menu from './comment.item__menu__.svelte';

	export let comment = {};
	export let comments = [];
	let error = '';

	const validate = async (vote) => {
		error = '';

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

			if (data.status == 200) {
				portal({
					for: 'comment',
					data: data.data.comments
				});
			} else {
				error = data.message;
			}
		}
	};

	let saturation = Math.floor(Math.random() * (360 + 1));

	let time = timeAgo(comment.created_at);
	onMount(() => {
		const intervalId = setInterval(() => {
			time = timeAgo(comment.created_at);
		}, 1000);

		return () => clearInterval(intervalId);
	});
</script>

<section>
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
		<div class="right">
			<div class="date">{time}</div>
			<div
				class="menu"
				on:keypress
				on:click={() => {
					$module = {
						module: Menu,
						comment
					};
				}}
			>
				&#8226;&#8226;&#8226;
			</div>
		</div>
	</div>
	<div>
		<div class="comment">
			<Marked md={comment.comment} />
		</div>
		{#if error}
			<span class="error">
				{error}
			</span>
			<br />
		{/if}
		{#if $_user.login}
			<div class="buttons">
				<Button
					icon="quote"
					class="secondary tiny"
					on:click={() => {
						$module = {
							module: Add_Comment,
							owner_key: comment.key
						};
					}}
				/>
				|
				<Button
					name={comment.downvote.length}
					class="secondary tiny"
					icon="dislike"
					on:click={() => {
						validate('down');
					}}
				/>
				|
				<Button
					name={comment.upvote.length}
					class="secondary tiny"
					icon="like"
					on:click={() => {
						validate('up');
					}}
				/>
			</div>
		{/if}
	</div>
	{#each comments as c}
		{#if c.path[c.path.length - 1] == comment.key}
			<Comment comment={c} {comments} />
		{/if}
	{/each}
</section>

<style>
	section {
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
	.right,
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
	.menu {
		cursor: pointer;
	}
	.menu:hover {
		color: var(--color1);
	}
	.comment,
	.name {
		color: var(--accent1);
	}

	.buttons {
		display: flex;
		gap: var(--gap1);
	}
</style>
