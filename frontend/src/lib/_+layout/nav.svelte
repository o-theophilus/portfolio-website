<script>
	import { module, app } from '$lib/store.svelte.js';

	import Link from './nav.btn.svelte';
	import User from './nav.user.svelte';
	import Notifications from './nav.notifications.svelte';
	import { Login } from '$lib/_authh';
	import Signup from '$lib/_auth/signup.svelte';
</script>

<nav>
	<div class="block">
		<a href="/">
			<img
				src={'/logo.png'}
				alt="logo"
				onerror={(e) => {
					const img = e.currentTarget;
					img.onerror = null;
					img.src = '/logo.png';
				}}
			/>
		</a>
		<div class="links">
			{#if app.user.login}
				<Notifications />
				<User />
			{:else}
				<Link onclick={() => module.open(Login)}>Login</Link>
				<Link onclick={() => module.open(Signup)}>Signup</Link>
			{/if}
		</div>
	</div>
</nav>

<style>
	nav {
		border-bottom: 1px solid var(--bg2);
	}
	.block {
		display: flex;
		height: var(--headerHeight);

		justify-content: space-between;
		align-items: center;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	img {
		height: 32px;
		display: block;
	}

	.links {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.block,
	.links {
		flex-wrap: wrap;
	}
</style>
