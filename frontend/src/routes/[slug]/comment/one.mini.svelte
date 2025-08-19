<script>
	import { Marked, Avatar } from '$lib/macro';
	let { comment } = $props();
</script>

<section>
	<div class="avatar_content">
		<Avatar name={comment.user.name} photo={comment.user.photo} />
		<div class="content">
			<div class="name">{comment.user.name}</div>
			<div class="comment">
				<Marked content={comment.comment} />
			</div>
		</div>
	</div>
</section>

<style>
	section {
		padding: var(--sp2);
		padding-right: 0;
		border: 2px solid var(--bg2);
		border-right-width: 0;
		margin-top: var(--sp2);
		border-top-left-radius: var(--sp0);
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
	}

	.comment {
		font-size: 0.8rem;
	}
</style>
