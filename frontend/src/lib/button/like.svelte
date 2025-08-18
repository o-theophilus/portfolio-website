<script>
	import { Icon } from '$lib/macro';

	let { active = '', like = 0, dislike = 0, onlike, ondislike } = $props();
</script>

<div class="group">
	<button class="like" onclick={onlike} class:active={active == 'like'}>
		<Icon icon="thumbs-up" />
		{like}
	</button>

	<button class="dislike" onclick={ondislike} class:active={active == 'dislike'}>
		<Icon icon="thumbs-down" />
		{dislike}
	</button>
</div>

<style>
	.group {
		display: flex;
		align-items: center;
		gap: 1px;
	}

	button {
		display: flex;
		align-items: center;
		gap: var(--sp0);

		height: var(--like-height, 48px);
		padding: var(--sp0) var(--sp2);
		font-size: 0.8rem;

		color: var(--ft2);
		background-color: var(--bg2);
		border: none;
		cursor: pointer;

		transition:
			background-color var(--trans),
			color var(--trans);
	}
	.like {
		border-radius: var(--like-height, 48px) 0 0 var(--like-height, 48px);
	}
	.dislike {
		border-radius: 0 var(--like-height, 48px) var(--like-height, 48px) 0;
	}

	button:hover {
		background-color: var(--cl1);
		color: white;
	}
</style>
