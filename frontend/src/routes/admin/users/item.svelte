<script>
	import { Avatar } from '$lib/macro';
	let { item } = $props();
</script>

<a href="/@{item.username}">
	<Avatar name={item.name} photo={item.photo} --avatar-border-radius="50%" />
	<div class="details">
		<div class="name">
			{item.name}
		</div>

		<span class="username">
			@{item.username}
		</span>
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--input);

		text-decoration: none;
		color: var(--ft2);
	}
	a:hover {
		text-decoration: none;
	}

	.details {
		width: 100%;
		line-height: 100%;
	}

	.name {
		font-weight: 700;
		color: var(--ft1);
	}
	.username {
		font-size: 0.7em;
	}

	span {
		word-wrap: break-word;
		word-break: break-all;
	}
</style>
