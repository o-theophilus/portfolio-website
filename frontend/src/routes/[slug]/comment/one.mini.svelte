<script>
	import { Marked, Avatar } from '$lib/macro';
	let { comment } = $props();
</script>

<section>
	<div class="avatar_content">
		<Avatar name={comment.user.name} photo={comment.user.photo} --avatar-border-radius="50%" />
		<div class="content">
			<div class="name">{comment.user.name}</div>
			<div class="comment">
				{comment.comment}
			</div>
		</div>
	</div>
</section>

<style>
	section {
		padding: var(--sp2);
		border: 2px solid var(--bg2);
		border-radius: var(--sp0);
	}

	.avatar_content {
		display: flex;
		gap: 16px;
	}

	.content {
		width: 100%;
	}

	.name {
		color: var(--ft1);
		font-size: 0.8rem;
		font-weight: 800;
		line-height: 100%;
	}

	.comment {
		font-size: 0.8rem;
		margin-top: 8px;
	}
</style>
