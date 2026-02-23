<script>
	import { page } from '$app/state';
	import { Avatar, Datetime } from '$lib/macro';
	import { onMount } from 'svelte';

	let { comment } = $props();
	console.log(comment);

	let _this;
	onMount(() => {
		if (page.url.hash == `#${comment.key}`) {
			_this.scrollIntoView({ behavior: 'smooth' });
		}
	});
</script>

<div class="avatar_name_date" bind:this={_this}>
	<Avatar name={comment.user.name} photo={comment.user.photo} --avatar-border-radius="50%" />

	<div class="name_date">
		<div class="name_username">
			<div class="name">{comment.user.name}</div>
			<div class="username">@{comment.user.username}</div>
		</div>
		<div class="date"><Datetime datetime={comment.date_created} type="ago" /></div>
	</div>
</div>

<div class="comment">
	{comment.comment}
</div>

<style>
	.avatar_name_date {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.name_date {
		display: flex;
		align-items: flex-start;
		gap: 8px 16px;
		justify-content: space-between;
		flex-wrap: wrap;

		width: 100%;
	}

	.name {
		color: var(--ft1);
		font-size: 0.8rem;
		font-weight: 800;
		line-height: 100%;
		margin-bottom: 4px;
	}

	.date {
		font-size: 0.7rem;
		line-height: 100%;
	}

	.username {
		font-size: 0.7rem;
	}

	.comment {
		font-size: 0.8rem;
		margin-top: 16px;
	}
</style>
