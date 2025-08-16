<script>
	import { Avatar } from '$lib/macro';
	let { user } = $props();
</script>

<a href="/@{user.key}">
	<Avatar name={user.name} photo={user.photo} />
	<div class="details">
		<div class="name">
			{user.name}
		</div>

		<span class="email">
			{user.email}
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
	.email {
		font-size: 0.8em;
	}

	span {
		word-wrap: break-word;
		word-break: break-all;
	}
</style>
