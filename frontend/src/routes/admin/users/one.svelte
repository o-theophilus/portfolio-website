<script>
	import { Avatar } from '$lib/macro';
	let { user } = $props();
</script>

<a href="/@{user.username}">
	<Avatar name={user.name} photo={user.photo} --avatar-border-radius="50%" />
	<div class="details">
		<div class="name">
			{user.name}
		</div>

		<span class="username">
			@{user.username}
		</span>
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: 16px;

		margin: 16px 0;
		padding-top: 16px;
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
