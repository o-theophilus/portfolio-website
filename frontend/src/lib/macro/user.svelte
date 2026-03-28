<script>
	import { Avatar } from '$lib/macro';
	let { user, children } = $props();
</script>

<div class="comp">
	<a href="/@{user.username}" class="avatar">
		<Avatar name={user.name} photo={user.photo} --avatar-border-radius="50%" />
	</a>

	<div class="name_username">
		<a href="/@{user.username}" class="name">{user.name}</a>
		<br />
		{@render children?.()}
	</div>
</div>

<style>
	.comp {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.8rem;
	}

	a {
		text-decoration: none;
		color: var(--ft2);
	}

	.name {
		color: var(--ft1);
		font-weight: 600;
	}
</style>
