<script>
	import { page } from '$app/state';
	import { Avatar, Datetime } from '$lib/macro';
	import { module } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	let { comment } = $props();

	let _this;
	onMount(() => {
		if (page.url.hash == `#${comment.key}`) {
			_this.scrollIntoView({ behavior: 'smooth' });
		}
	});
</script>

<div class="comment_area">
	<div class="avatar_name_date" bind:this={_this}>
		<a href="@{comment.user.username}" class="img" onclick={() => module.close()}>
			<Avatar name={comment.user.name} photo={comment.user.photo} --avatar-border-radius="50%" />
		</a>

		<div class="name_date">
			<div class="name_username">
				<a href="@{comment.user.username}" class="name" onclick={() => module.close()}>
					{comment.user.name}
				</a>
				<a href="@{comment.user.username}" class="username" onclick={() => module.close()}>
					@{comment.user.username}
				</a>
			</div>
			<div class="date"><Datetime datetime={comment.date_created} type="ago" /></div>
		</div>
	</div>

	{#if comment.comment}
		<div class="comment">
			{comment.comment}
		</div>
	{/if}
</div>

<style>
	.comment_area {
		width: 100%;
	}

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

		.name_username {
			display: flex;
			flex-direction: column;

			.name {
				color: var(--ft1);
				font-size: 0.8rem;
				font-weight: 800;
				line-height: 100%;
				margin-bottom: 4px;
			}

			.username {
				font-size: 0.7rem;
				color: var(--ft2);
			}
		}

		.date {
			font-size: 0.7rem;
			line-height: 100%;
		}
	}

	.comment {
		font-size: 0.8rem;
		margin-top: 16px;
	}

	a {
		text-decoration: none;

		&.img {
			border-radius: 50%;
		}
	}
</style>
