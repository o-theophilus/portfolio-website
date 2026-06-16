<script>
	import { Tag } from '$lib/button';
	import { Avatar } from '$lib/macro';
	let { user, all = false } = $props();
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

	{#if user.blocked}
		<Tag>Blocked</Tag>
	{:else if all}
		<Tag>{user.status}</Tag>
	{/if}
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: 16px;

		margin-top: 8px;
		padding: 16px;
		background-color: var(--bg3);
		border-radius: 8px;

		text-decoration: none;
		color: var(--ft2);
		text-decoration: none;
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}

		& .details {
			width: 100%;
			line-height: 100%;

			& .name {
				font-weight: 700;
				color: var(--ft1);
			}

			& .username {
				font-size: 0.7em;
			}
		}

		--tag-font-size: 0.7rem;
	}
</style>
