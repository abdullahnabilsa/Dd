#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_1a.py
=================
Phase 1A: Configuration + Database + Utilities + Types
Creates all foundational files for the AI Chat Platform.
"""

import os

files_created = 0
files_failed = 0


def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    global files_created, files_failed
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_created += 1
        print(f"  ✅ Created: {path}")
    except Exception as e:
        files_failed += 1
        print(f"  ❌ Failed: {path} - {e}")


def main():
    global files_created, files_failed

    print("=" * 60)
    print("🚀 BUILD PHASE 1A: Configuration + Database + Utilities + Types")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # GROUP A: Configuration (7 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group A: Configuration Files")
    print("-" * 40)

    # 1. package.json
    create_file("package.json", '''{
  "name": "ai-chat-platform",
  "version": "1.0.0",
  "private": true,
  "description": "Professional Multi-Platform AI Chat Platform with Personas",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "pages:build": "npx @cloudflare/next-on-pages",
    "pages:dev": "npx wrangler pages dev .vercel/output/static --compatibility-date=2024-01-01",
    "deploy": "npm run pages:build && npx wrangler pages deploy .vercel/output/static"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "@supabase/supabase-js": "^2.45.0",
    "@supabase/auth-helpers-nextjs": "^0.10.0",
    "@supabase/ssr": "^0.5.0",
    "zustand": "^4.5.0",
    "ai": "^3.3.0",
    "@ai-sdk/openai": "^0.0.60",
    "next-intl": "^3.20.0",
    "react-markdown": "^9.0.0",
    "rehype-highlight": "^7.0.0",
    "jspdf": "^2.5.0",
    "file-saver": "^2.0.5",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.5.0",
    "lucide-react": "^0.440.0",
    "class-variance-authority": "^0.7.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@types/node": "^22.0.0",
    "@types/file-saver": "^2.0.7",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "@cloudflare/next-on-pages": "^1.13.0",
    "wrangler": "^3.70.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0"
  }
}
''')

    # 2. next.config.js
    create_file("next.config.js", """// إعدادات Next.js 14 مع دعم Cloudflare Pages و next-intl
const createNextIntlPlugin = require('next-intl/plugin');

const withNextIntl = createNextIntlPlugin('./i18n/config.ts');

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    unoptimized: true,
  },
  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000'],
    },
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
};

module.exports = withNextIntl(nextConfig);
""")

    # 3. tailwind.config.ts
    create_file("tailwind.config.ts", """// إعدادات Tailwind CSS مع الثيم البنفسجي ودعم الوضع المظلم
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
    './hooks/**/*.{ts,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0effe',
          100: '#e0dffd',
          200: '#c2bffb',
          300: '#a39ff9',
          400: '#857ff7',
          500: '#6c63ff',
          600: '#5650e6',
          700: '#413dcc',
          800: '#2b29b3',
          900: '#161699',
          DEFAULT: '#6c63ff',
        },
        secondary: {
          50: '#e6fbff',
          100: '#ccf7ff',
          200: '#99efff',
          300: '#66e7ff',
          400: '#33dfff',
          500: '#00d2ff',
          600: '#00a8cc',
          700: '#007e99',
          800: '#005466',
          900: '#002a33',
          DEFAULT: '#00d2ff',
        },
        accent: {
          50: '#fef0f5',
          100: '#fde1eb',
          200: '#fbc3d7',
          300: '#f9a5c3',
          400: '#f787af',
          500: '#f72585',
          600: '#c61e6a',
          700: '#941750',
          800: '#630f35',
          900: '#31081b',
          DEFAULT: '#f72585',
        },
        dark: {
          50: '#f7f7f8',
          100: '#ededf0',
          200: '#d4d4db',
          300: '#b0b0bd',
          400: '#8c8c9e',
          500: '#6e6e82',
          600: '#57576b',
          700: '#3d3d50',
          800: '#2a2a3c',
          900: '#1a1a2e',
          950: '#0f0f1a',
          DEFAULT: '#1a1a2e',
        },
      },
      fontFamily: {
        'sans-arabic': ['Cairo', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-in-right': 'slideInRight 0.3s ease-in-out',
        'slide-in-left': 'slideInLeft 0.3s ease-in-out',
        'blink': 'blink 1s step-end infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
      },
      spacing: {
        'sidebar': '280px',
      },
      zIndex: {
        'sidebar': '40',
        'header': '30',
        'overlay': '50',
        'modal': '60',
        'toast': '70',
      },
    },
  },
  plugins: [],
};

export default config;
""")

    # 4. tsconfig.json
    create_file("tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    },
    "forceConsistentCasingInFileNames": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules", "workers"]
}
""")

    # 5. wrangler.toml
    create_file("wrangler.toml", """# إعدادات Cloudflare Worker للبروكسي
name = "ai-chat-proxy"
main = "workers/proxy.ts"
compatibility_date = "2024-01-01"
compatibility_flags = ["nodejs_compat"]

[vars]
ENVIRONMENT = "production"

# [secrets]
# ENCRYPTION_KEY - set via wrangler secret put
""")

    # 6. .env.example
    create_file(".env.example", """# ====================================
# AI Chat Platform - Environment Variables
# ====================================

# Supabase Configuration
# Get from: https://app.supabase.com/project/YOUR_PROJECT/settings/api
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Supabase Service Role Key (server-side only, NEVER expose to client)
# Get from: https://app.supabase.com/project/YOUR_PROJECT/settings/api
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Encryption Key for API Keys (exactly 32 characters for AES-256)
# Generate with: openssl rand -hex 16
ENCRYPTION_KEY=your32characterencryptionkeyhere

# Telegram Bot for Notifications
# Create bot via @BotFather on Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=-1001234567890

# Super Admin Account (created automatically on first registration)
SUPER_ADMIN_EMAIL=admin@example.com
SUPER_ADMIN_PASSWORD=YourSecurePassword123!

# Application Settings
NEXT_PUBLIC_APP_NAME=AI Chat Platform
NEXT_PUBLIC_APP_URL=https://your-domain.pages.dev
""")

    # 7. middleware.ts
    create_file("middleware.ts", """// الوسيط الرئيسي: حماية المسارات، التحقق من الجلسة، توجيه اللغة، حماية لوحة الإدارة
import { createServerClient, type CookieOptions } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';
import createMiddleware from 'next-intl/middleware';

const intlMiddleware = createMiddleware({
  locales: ['ar', 'en'],
  defaultLocale: 'ar',
  localeDetection: true,
  localePrefix: 'always',
});

const PUBLIC_PATHS = ['/login', '/register', '/invite'];
const PROTECTED_PATHS = ['/chat', '/personas', '/settings', '/admin'];
const ADMIN_PATHS = ['/admin'];

function isPublicPath(pathname: string): boolean {
  return PUBLIC_PATHS.some((path) => pathname.includes(path));
}

function isProtectedPath(pathname: string): boolean {
  return PROTECTED_PATHS.some((path) => pathname.includes(path));
}

function isAdminPath(pathname: string): boolean {
  return ADMIN_PATHS.some((path) => pathname.includes(path));
}

function getPathWithoutLocale(pathname: string): string {
  const segments = pathname.split('/');
  if (segments.length > 1 && (segments[1] === 'ar' || segments[1] === 'en')) {
    return '/' + segments.slice(2).join('/');
  }
  return pathname;
}

function getLocaleFromPath(pathname: string): string {
  const segments = pathname.split('/');
  if (segments.length > 1 && (segments[1] === 'ar' || segments[1] === 'en')) {
    return segments[1];
  }
  return 'ar';
}

export async function middleware(request: NextRequest): Promise<NextResponse> {
  const { pathname } = request.nextUrl;

  if (
    pathname.startsWith('/api/') ||
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/favicon') ||
    pathname.includes('.')
  ) {
    return NextResponse.next();
  }

  const pathWithoutLocale = getPathWithoutLocale(pathname);
  const locale = getLocaleFromPath(pathname);

  let response = intlMiddleware(request);

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({ name, value, ...options });
          response = NextResponse.next({
            request: { headers: request.headers },
          });
          response.cookies.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({ name, value: '', ...options });
          response = NextResponse.next({
            request: { headers: request.headers },
          });
          response.cookies.set({ name, value: '', ...options });
        },
      },
    }
  );

  try {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session && isProtectedPath(pathWithoutLocale)) {
      const loginUrl = new URL(`/${locale}/login`, request.url);
      loginUrl.searchParams.set('redirect', pathname);
      return NextResponse.redirect(loginUrl);
    }

    if (session && isPublicPath(pathWithoutLocale)) {
      const chatUrl = new URL(`/${locale}/chat`, request.url);
      return NextResponse.redirect(chatUrl);
    }

    if (session && isAdminPath(pathWithoutLocale)) {
      const { data: profile } = await supabase
        .from('profiles')
        .select('role, is_banned')
        .eq('id', session.user.id)
        .single();

      if (!profile || profile.role !== 'admin') {
        const chatUrl = new URL(`/${locale}/chat`, request.url);
        return NextResponse.redirect(chatUrl);
      }

      if (profile.is_banned) {
        await supabase.auth.signOut();
        const loginUrl = new URL(`/${locale}/login`, request.url);
        return NextResponse.redirect(loginUrl);
      }
    }

    if (session && isProtectedPath(pathWithoutLocale) && !isAdminPath(pathWithoutLocale)) {
      const { data: profile } = await supabase
        .from('profiles')
        .select('is_banned')
        .eq('id', session.user.id)
        .single();

      if (profile?.is_banned) {
        await supabase.auth.signOut();
        const loginUrl = new URL(`/${locale}/login`, request.url);
        return NextResponse.redirect(loginUrl);
      }
    }
  } catch (error) {
    if (isProtectedPath(pathWithoutLocale)) {
      const loginUrl = new URL(`/${locale}/login`, request.url);
      return NextResponse.redirect(loginUrl);
    }
  }

  return response;
}

export const config = {
  matcher: ['/((?!_next|api|favicon.ico|icons|persona-icons|robots.txt|manifest.json).*)'],
};
""")

    # ──────────────────────────────────────────────
    # GROUP B: Database (4 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group B: Database Files")
    print("-" * 40)

    # 8. supabase/schema.sql
    create_file("supabase/schema.sql", """-- مخطط قاعدة البيانات الكامل: 14 جدول لمنصة الدردشة بالذكاء الاصطناعي
-- يتضمن جميع الأعمدة والقيود والمفاتيح الخارجية والفهارس

-- ============================================
-- تفعيل الامتدادات المطلوبة
-- ============================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- 1. جدول الملفات الشخصية (profiles)
-- ============================================
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    role TEXT NOT NULL DEFAULT 'free' CHECK (role IN ('admin', 'premium', 'free')),
    is_super_admin BOOLEAN NOT NULL DEFAULT false,
    premium_expires_at TIMESTAMPTZ,
    trial_used BOOLEAN NOT NULL DEFAULT false,
    trial_expires_at TIMESTAMPTZ,
    is_banned BOOLEAN NOT NULL DEFAULT false,
    onboarding_completed BOOLEAN NOT NULL DEFAULT false,
    preferred_language TEXT NOT NULL DEFAULT 'ar',
    preferred_theme TEXT NOT NULL DEFAULT 'dark',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_profiles_email ON profiles(email);
CREATE INDEX idx_profiles_role ON profiles(role);
CREATE INDEX idx_profiles_is_super_admin ON profiles(is_super_admin);

-- ============================================
-- 2. جدول المجلدات (folders)
-- ============================================
CREATE TABLE IF NOT EXISTS folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('auto', 'custom')),
    persona_id UUID,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_folders_user_id ON folders(user_id);

-- ============================================
-- 3. جدول الشخصيات (personas)
-- ============================================
CREATE TABLE IF NOT EXISTS personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    icon_url TEXT,
    category TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('system', 'premium', 'custom', 'shared')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_approved BOOLEAN NOT NULL DEFAULT false,
    average_rating DECIMAL(2,1) NOT NULL DEFAULT 0,
    rating_count INTEGER NOT NULL DEFAULT 0,
    usage_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_personas_type ON personas(type);
CREATE INDEX idx_personas_category ON personas(category);
CREATE INDEX idx_personas_is_active ON personas(is_active);
CREATE INDEX idx_personas_user_id ON personas(user_id);

-- إضافة المرجع الخارجي للمجلدات بعد إنشاء جدول الشخصيات
ALTER TABLE folders ADD CONSTRAINT fk_folders_persona_id
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE SET NULL;

-- ============================================
-- 4. جدول المحادثات (conversations)
-- ============================================
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT 'محادثة جديدة',
    persona_id UUID REFERENCES personas(id) ON DELETE SET NULL,
    platform TEXT NOT NULL,
    model TEXT NOT NULL,
    folder_id UUID REFERENCES folders(id) ON DELETE SET NULL,
    is_favorited BOOLEAN NOT NULL DEFAULT false,
    message_count INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_folder_id ON conversations(folder_id);
CREATE INDEX idx_conversations_persona_id ON conversations(persona_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- ============================================
-- 5. جدول الرسائل (messages)
-- ============================================
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    model TEXT,
    platform TEXT,
    persona_name TEXT,
    tokens_used INTEGER NOT NULL DEFAULT 0,
    response_time_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_role ON messages(role);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- ============================================
-- 6. جدول تقييمات الشخصيات (persona_ratings)
-- ============================================
CREATE TABLE IF NOT EXISTS persona_ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (persona_id, user_id)
);

CREATE INDEX idx_persona_ratings_persona_id ON persona_ratings(persona_id);
CREATE INDEX idx_persona_ratings_user_id ON persona_ratings(user_id);

-- ============================================
-- 7. جدول مفاتيح API (api_keys)
-- ============================================
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    encrypted_key TEXT NOT NULL,
    label TEXT NOT NULL,
    is_global BOOLEAN NOT NULL DEFAULT false,
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_platform ON api_keys(platform);
CREATE INDEX idx_api_keys_is_global ON api_keys(is_global);

-- ============================================
-- 8. جدول النماذج العامة (global_models)
-- ============================================
CREATE TABLE IF NOT EXISTS global_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_key_id UUID NOT NULL REFERENCES api_keys(id) ON DELETE CASCADE,
    model_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_global_models_api_key_id ON global_models(api_key_id);
CREATE INDEX idx_global_models_is_active ON global_models(is_active);
CREATE INDEX idx_global_models_sort_order ON global_models(sort_order);

-- ============================================
-- 9. جدول أكواد الدعوة (invite_codes)
-- ============================================
CREATE TABLE IF NOT EXISTS invite_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT NOT NULL UNIQUE,
    created_by UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    max_uses INTEGER NOT NULL DEFAULT 1,
    current_uses INTEGER NOT NULL DEFAULT 0,
    premium_duration_days INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT true,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_invite_codes_code ON invite_codes(code);
CREATE INDEX idx_invite_codes_is_active ON invite_codes(is_active);

-- ============================================
-- 10. جدول استخدامات أكواد الدعوة (invite_code_uses)
-- ============================================
CREATE TABLE IF NOT EXISTS invite_code_uses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invite_code_id UUID NOT NULL REFERENCES invite_codes(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    used_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (invite_code_id, user_id)
);

CREATE INDEX idx_invite_code_uses_invite_code_id ON invite_code_uses(invite_code_id);
CREATE INDEX idx_invite_code_uses_user_id ON invite_code_uses(user_id);

-- ============================================
-- 11. جدول الإشعارات (notifications)
-- ============================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'normal' CHECK (priority IN ('urgent', 'normal', 'info')),
    is_read BOOLEAN NOT NULL DEFAULT false,
    related_user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

-- ============================================
-- 12. جدول تجارب الشخصيات المميزة (premium_persona_trials)
-- ============================================
CREATE TABLE IF NOT EXISTS premium_persona_trials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    used_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, persona_id)
);

CREATE INDEX idx_premium_persona_trials_user_id ON premium_persona_trials(user_id);
CREATE INDEX idx_premium_persona_trials_persona_id ON premium_persona_trials(persona_id);

-- ============================================
-- 13. جدول المفضلات (user_favorites)
-- ============================================
CREATE TABLE IF NOT EXISTS user_favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    item_type TEXT NOT NULL CHECK (item_type IN ('persona', 'model')),
    item_id TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, item_type, item_id)
);

CREATE INDEX idx_user_favorites_user_id ON user_favorites(user_id);
CREATE INDEX idx_user_favorites_item_type ON user_favorites(item_type);

-- ============================================
-- 14. جدول إحصائيات الاستخدام (usage_stats)
-- ============================================
CREATE TABLE IF NOT EXISTS usage_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    messages_sent INTEGER NOT NULL DEFAULT 0,
    tokens_used INTEGER NOT NULL DEFAULT 0,
    conversations_created INTEGER NOT NULL DEFAULT 0,
    persona_id_most_used UUID REFERENCES personas(id) ON DELETE SET NULL,
    UNIQUE (user_id, date)
);

CREATE INDEX idx_usage_stats_user_id ON usage_stats(user_id);
CREATE INDEX idx_usage_stats_date ON usage_stats(date);

-- ============================================
-- تحديث updated_at تلقائياً
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_personas_updated_at
    BEFORE UPDATE ON personas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
""")

    # 9. supabase/rls-policies.sql
    create_file("supabase/rls-policies.sql", """-- سياسات أمان مستوى الصف (RLS) لجميع الجداول الـ 14
-- يجب تفعيل RLS على كل جدول وإنشاء سياسات محددة لكل عملية

-- ============================================
-- تفعيل RLS على جميع الجداول
-- ============================================
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE personas ENABLE ROW LEVEL SECURITY;
ALTER TABLE persona_ratings ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE global_models ENABLE ROW LEVEL SECURITY;
ALTER TABLE folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE invite_codes ENABLE ROW LEVEL SECURITY;
ALTER TABLE invite_code_uses ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE premium_persona_trials ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_stats ENABLE ROW LEVEL SECURITY;

-- ============================================
-- دالة مساعدة: هل المستخدم مدير؟
-- ============================================
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM profiles
        WHERE id = auth.uid()
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- دالة مساعدة: هل المستخدم مدير خارق؟
CREATE OR REPLACE FUNCTION is_super_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM profiles
        WHERE id = auth.uid()
        AND is_super_admin = true
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- دالة مساعدة: ما هو دور المستخدم؟
CREATE OR REPLACE FUNCTION get_user_role()
RETURNS TEXT AS $$
DECLARE
    user_role TEXT;
BEGIN
    SELECT role INTO user_role FROM profiles WHERE id = auth.uid();
    RETURN COALESCE(user_role, 'free');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- سياسات جدول profiles
-- ============================================
-- القراءة: المستخدم يرى ملفه فقط، المدير يرى الجميع
CREATE POLICY "profiles_select_own" ON profiles
    FOR SELECT USING (id = auth.uid());

CREATE POLICY "profiles_select_admin" ON profiles
    FOR SELECT USING (is_admin());

-- الإدراج: فقط عبر الـ trigger (handle_new_user)
-- لا سياسة INSERT للمستخدمين العاديين - يتم عبر service role

-- التحديث: المستخدم يحدث ملفه (بدون role/super/ban)، المدير يحدث الجميع
CREATE POLICY "profiles_update_own" ON profiles
    FOR UPDATE USING (id = auth.uid())
    WITH CHECK (
        id = auth.uid()
        AND role = (SELECT role FROM profiles WHERE id = auth.uid())
        AND is_super_admin = (SELECT is_super_admin FROM profiles WHERE id = auth.uid())
        AND is_banned = (SELECT is_banned FROM profiles WHERE id = auth.uid())
    );

CREATE POLICY "profiles_update_admin" ON profiles
    FOR UPDATE USING (is_admin())
    WITH CHECK (is_admin());

-- الحذف: المدير فقط (باستثناء المدير الخارق)
CREATE POLICY "profiles_delete_admin" ON profiles
    FOR DELETE USING (
        is_admin()
        AND NOT (SELECT is_super_admin FROM profiles WHERE id = profiles.id)
    );

-- ============================================
-- سياسات جدول conversations
-- ============================================
CREATE POLICY "conversations_select_own" ON conversations
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "conversations_insert_own" ON conversations
    FOR INSERT WITH CHECK (
        user_id = auth.uid()
        AND (
            get_user_role() != 'free'
            OR (SELECT COUNT(*) FROM conversations WHERE user_id = auth.uid()) < 20
        )
    );

CREATE POLICY "conversations_update_own" ON conversations
    FOR UPDATE USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "conversations_delete_own" ON conversations
    FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "conversations_delete_admin" ON conversations
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول messages
-- ============================================
CREATE POLICY "messages_select_own" ON messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM conversations
            WHERE conversations.id = messages.conversation_id
            AND conversations.user_id = auth.uid()
        )
    );

CREATE POLICY "messages_insert_own" ON messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM conversations
            WHERE conversations.id = messages.conversation_id
            AND conversations.user_id = auth.uid()
        )
    );

CREATE POLICY "messages_delete_own" ON messages
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM conversations
            WHERE conversations.id = messages.conversation_id
            AND conversations.user_id = auth.uid()
        )
    );

CREATE POLICY "messages_delete_admin" ON messages
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول personas
-- ============================================
-- القراءة: الشخصيات النظامية والمميزة والمشتركة المعتمدة للجميع
-- الشخصيات المخصصة لصاحبها فقط، المدير يرى الكل
CREATE POLICY "personas_select_public" ON personas
    FOR SELECT USING (
        type IN ('system', 'premium')
        AND is_active = true
    );

CREATE POLICY "personas_select_shared_approved" ON personas
    FOR SELECT USING (
        type = 'shared'
        AND is_approved = true
        AND is_active = true
    );

CREATE POLICY "personas_select_own" ON personas
    FOR SELECT USING (
        type = 'custom'
        AND user_id = auth.uid()
    );

CREATE POLICY "personas_select_admin" ON personas
    FOR SELECT USING (is_admin());

-- الإدراج: المستخدم ينشئ مخصصة (حد 4 للمجاني)، المدير ينشئ أي نوع
CREATE POLICY "personas_insert_own" ON personas
    FOR INSERT WITH CHECK (
        user_id = auth.uid()
        AND type IN ('custom', 'shared')
        AND (
            get_user_role() != 'free'
            OR (SELECT COUNT(*) FROM personas WHERE user_id = auth.uid() AND type = 'custom') < 4
        )
    );

CREATE POLICY "personas_insert_admin" ON personas
    FOR INSERT WITH CHECK (is_admin());

-- التحديث: صاحب المخصصة يحدثها، المدير يحدث الكل
CREATE POLICY "personas_update_own" ON personas
    FOR UPDATE USING (
        user_id = auth.uid()
        AND type IN ('custom', 'shared')
    )
    WITH CHECK (
        user_id = auth.uid()
        AND type IN ('custom', 'shared')
    );

CREATE POLICY "personas_update_admin" ON personas
    FOR UPDATE USING (is_admin())
    WITH CHECK (is_admin());

-- الحذف: صاحب المخصصة يحذفها، المدير يحذف (باستثناء الـ 4 الأصلية)
CREATE POLICY "personas_delete_own" ON personas
    FOR DELETE USING (
        user_id = auth.uid()
        AND type IN ('custom', 'shared')
    );

CREATE POLICY "personas_delete_admin" ON personas
    FOR DELETE USING (
        is_admin()
        AND type != 'system'
    );

-- ============================================
-- سياسات جدول persona_ratings
-- ============================================
CREATE POLICY "persona_ratings_select_all" ON persona_ratings
    FOR SELECT USING (true);

CREATE POLICY "persona_ratings_insert_own" ON persona_ratings
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "persona_ratings_update_own" ON persona_ratings
    FOR UPDATE USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "persona_ratings_delete_own" ON persona_ratings
    FOR DELETE USING (user_id = auth.uid());

-- ============================================
-- سياسات جدول api_keys
-- ============================================
-- القراءة: المستخدم يرى مفاتيحه، المفاتيح العامة (platform+label فقط)، المدير يرى الكل
CREATE POLICY "api_keys_select_own" ON api_keys
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "api_keys_select_global_limited" ON api_keys
    FOR SELECT USING (is_global = true);

CREATE POLICY "api_keys_select_admin" ON api_keys
    FOR SELECT USING (is_admin());

-- الإدراج: المستخدم ينشئ (حد 2 للمجاني)، المدير ينشئ عامة
CREATE POLICY "api_keys_insert_own" ON api_keys
    FOR INSERT WITH CHECK (
        user_id = auth.uid()
        AND is_global = false
        AND (
            get_user_role() != 'free'
            OR (SELECT COUNT(*) FROM api_keys WHERE user_id = auth.uid() AND is_global = false) < 2
        )
    );

CREATE POLICY "api_keys_insert_admin" ON api_keys
    FOR INSERT WITH CHECK (is_admin());

-- التحديث: صاحب المفتاح أو المدير للعامة
CREATE POLICY "api_keys_update_own" ON api_keys
    FOR UPDATE USING (user_id = auth.uid() AND is_global = false)
    WITH CHECK (user_id = auth.uid() AND is_global = false);

CREATE POLICY "api_keys_update_admin" ON api_keys
    FOR UPDATE USING (is_admin())
    WITH CHECK (is_admin());

-- الحذف: صاحب المفتاح أو المدير
CREATE POLICY "api_keys_delete_own" ON api_keys
    FOR DELETE USING (user_id = auth.uid() AND is_global = false);

CREATE POLICY "api_keys_delete_admin" ON api_keys
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول global_models
-- ============================================
CREATE POLICY "global_models_select_active" ON global_models
    FOR SELECT USING (is_active = true);

CREATE POLICY "global_models_select_admin" ON global_models
    FOR SELECT USING (is_admin());

CREATE POLICY "global_models_insert_admin" ON global_models
    FOR INSERT WITH CHECK (is_admin());

CREATE POLICY "global_models_update_admin" ON global_models
    FOR UPDATE USING (is_admin())
    WITH CHECK (is_admin());

CREATE POLICY "global_models_delete_admin" ON global_models
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول folders
-- ============================================
CREATE POLICY "folders_select_own" ON folders
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "folders_insert_own" ON folders
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "folders_update_own" ON folders
    FOR UPDATE USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "folders_delete_own" ON folders
    FOR DELETE USING (user_id = auth.uid());

-- ============================================
-- سياسات جدول invite_codes
-- ============================================
CREATE POLICY "invite_codes_select_admin" ON invite_codes
    FOR SELECT USING (is_admin());

CREATE POLICY "invite_codes_insert_admin" ON invite_codes
    FOR INSERT WITH CHECK (is_admin());

CREATE POLICY "invite_codes_update_admin" ON invite_codes
    FOR UPDATE USING (is_admin())
    WITH CHECK (is_admin());

CREATE POLICY "invite_codes_delete_admin" ON invite_codes
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول invite_code_uses
-- ============================================
CREATE POLICY "invite_code_uses_select_admin" ON invite_code_uses
    FOR SELECT USING (is_admin());

CREATE POLICY "invite_code_uses_delete_admin" ON invite_code_uses
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول notifications
-- ============================================
CREATE POLICY "notifications_select_admin" ON notifications
    FOR SELECT USING (is_admin());

CREATE POLICY "notifications_update_admin" ON notifications
    FOR UPDATE USING (is_admin())
    WITH CHECK (is_admin());

CREATE POLICY "notifications_delete_admin" ON notifications
    FOR DELETE USING (is_admin());

-- ============================================
-- سياسات جدول premium_persona_trials
-- ============================================
CREATE POLICY "premium_persona_trials_select_own" ON premium_persona_trials
    FOR SELECT USING (user_id = auth.uid());

-- ============================================
-- سياسات جدول user_favorites
-- ============================================
CREATE POLICY "user_favorites_select_own" ON user_favorites
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "user_favorites_insert_own" ON user_favorites
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "user_favorites_update_own" ON user_favorites
    FOR UPDATE USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "user_favorites_delete_own" ON user_favorites
    FOR DELETE USING (user_id = auth.uid());

-- ============================================
-- سياسات جدول usage_stats
-- ============================================
CREATE POLICY "usage_stats_select_own" ON usage_stats
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "usage_stats_select_admin" ON usage_stats
    FOR SELECT USING (is_admin());

CREATE POLICY "usage_stats_delete_admin" ON usage_stats
    FOR DELETE USING (is_admin());
""")

    # 10. supabase/functions.sql
    create_file("supabase/functions.sql", """-- دوال قاعدة البيانات السبع مع المشغلات (Triggers)
-- تتعامل مع إنشاء المستخدمين، تحديث العدادات، التقييمات، انتهاء الصلاحية

-- ============================================
-- 1. دالة معالجة المستخدم الجديد
-- يتم تشغيلها بعد إدراج مستخدم جديد في auth.users
-- ============================================
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
    super_admin_email TEXT;
    user_role TEXT DEFAULT 'free';
    user_is_super BOOLEAN DEFAULT false;
BEGIN
    -- الحصول على بريد المدير الخارق من إعدادات التطبيق
    super_admin_email := current_setting('app.super_admin_email', true);

    -- التحقق إذا كان هذا هو المدير الخارق
    IF NEW.email = super_admin_email THEN
        user_role := 'admin';
        user_is_super := true;
    END IF;

    -- إنشاء الملف الشخصي
    INSERT INTO profiles (id, email, display_name, role, is_super_admin)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'display_name', split_part(NEW.email, '@', 1)),
        user_role,
        user_is_super
    );

    -- إنشاء إشعار تسجيل مستخدم جديد
    INSERT INTO notifications (type, title, message, priority, related_user_id, metadata)
    VALUES (
        'user_registered',
        'مستخدم جديد',
        'تم تسجيل مستخدم جديد: ' || NEW.email,
        'info',
        NEW.id,
        jsonb_build_object('email', NEW.email, 'role', user_role)
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء المشغل
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- ============================================
-- 2. دالة تحديث عدد رسائل المحادثة
-- يتم تشغيلها بعد إدراج رسالة بدور 'user'
-- ============================================
CREATE OR REPLACE FUNCTION update_conversation_message_count()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role = 'user' THEN
        UPDATE conversations
        SET message_count = message_count + 1,
            updated_at = now()
        WHERE id = NEW.conversation_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_message_inserted_count ON messages;
CREATE TRIGGER on_message_inserted_count
    AFTER INSERT ON messages
    FOR EACH ROW EXECUTE FUNCTION update_conversation_message_count();

-- ============================================
-- 3. دالة تحديث عدد الرموز في المحادثة
-- يتم تشغيلها بعد إدراج رسالة بدور 'assistant'
-- ============================================
CREATE OR REPLACE FUNCTION update_conversation_tokens()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role = 'assistant' AND NEW.tokens_used > 0 THEN
        UPDATE conversations
        SET total_tokens = total_tokens + NEW.tokens_used,
            updated_at = now()
        WHERE id = NEW.conversation_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_message_inserted_tokens ON messages;
CREATE TRIGGER on_message_inserted_tokens
    AFTER INSERT ON messages
    FOR EACH ROW EXECUTE FUNCTION update_conversation_tokens();

-- ============================================
-- 4. دالة تحديث تقييم الشخصية
-- يتم تشغيلها بعد INSERT/UPDATE/DELETE على persona_ratings
-- ============================================
CREATE OR REPLACE FUNCTION update_persona_rating()
RETURNS TRIGGER AS $$
DECLARE
    target_persona_id UUID;
    new_avg DECIMAL(2,1);
    new_count INTEGER;
BEGIN
    -- تحديد الشخصية المستهدفة
    IF TG_OP = 'DELETE' THEN
        target_persona_id := OLD.persona_id;
    ELSE
        target_persona_id := NEW.persona_id;
    END IF;

    -- حساب المتوسط والعدد الجديد
    SELECT
        COALESCE(ROUND(AVG(rating)::numeric, 1), 0),
        COUNT(*)
    INTO new_avg, new_count
    FROM persona_ratings
    WHERE persona_id = target_persona_id;

    -- تحديث الشخصية
    UPDATE personas
    SET average_rating = new_avg,
        rating_count = new_count,
        updated_at = now()
    WHERE id = target_persona_id;

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_persona_rating_changed ON persona_ratings;
CREATE TRIGGER on_persona_rating_changed
    AFTER INSERT OR UPDATE OR DELETE ON persona_ratings
    FOR EACH ROW EXECUTE FUNCTION update_persona_rating();

-- ============================================
-- 5. دالة فحص انتهاء صلاحية الاشتراك المميز
-- يتم تشغيلها دورياً (عبر cron أو استدعاء يدوي)
-- ============================================
CREATE OR REPLACE FUNCTION check_premium_expiry()
RETURNS INTEGER AS $$
DECLARE
    expired_count INTEGER := 0;
    expired_user RECORD;
BEGIN
    FOR expired_user IN
        SELECT id, email
        FROM profiles
        WHERE role = 'premium'
        AND premium_expires_at IS NOT NULL
        AND premium_expires_at < now()
    LOOP
        -- تحويل المستخدم إلى مجاني
        UPDATE profiles
        SET role = 'free',
            premium_expires_at = NULL,
            updated_at = now()
        WHERE id = expired_user.id;

        -- إنشاء إشعار
        INSERT INTO notifications (type, title, message, priority, related_user_id, metadata)
        VALUES (
            'premium_expired',
            'انتهاء الاشتراك المميز',
            'انتهت صلاحية الاشتراك المميز للمستخدم: ' || expired_user.email,
            'normal',
            expired_user.id,
            jsonb_build_object('email', expired_user.email)
        );

        expired_count := expired_count + 1;
    END LOOP;

    RETURN expired_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- 6. دالة فحص انتهاء الفترة التجريبية
-- يتم تشغيلها دورياً (عبر cron أو استدعاء يدوي)
-- ============================================
CREATE OR REPLACE FUNCTION check_trial_expiry()
RETURNS INTEGER AS $$
DECLARE
    expired_count INTEGER := 0;
    expired_user RECORD;
BEGIN
    FOR expired_user IN
        SELECT id, email
        FROM profiles
        WHERE role = 'premium'
        AND trial_expires_at IS NOT NULL
        AND trial_expires_at < now()
    LOOP
        -- تحويل المستخدم إلى مجاني وتعليم التجربة كمستخدمة
        UPDATE profiles
        SET role = 'free',
            trial_used = true,
            trial_expires_at = NULL,
            premium_expires_at = NULL,
            updated_at = now()
        WHERE id = expired_user.id;

        -- إنشاء إشعار
        INSERT INTO notifications (type, title, message, priority, related_user_id, metadata)
        VALUES (
            'trial_expired',
            'انتهاء الفترة التجريبية',
            'انتهت الفترة التجريبية للمستخدم: ' || expired_user.email,
            'normal',
            expired_user.id,
            jsonb_build_object('email', expired_user.email)
        );

        expired_count := expired_count + 1;
    END LOOP;

    RETURN expired_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- 7. دالة زيادة عداد استخدام الشخصية
-- يتم تشغيلها بعد إنشاء محادثة مع شخصية
-- ============================================
CREATE OR REPLACE FUNCTION increment_persona_usage()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.persona_id IS NOT NULL THEN
        UPDATE personas
        SET usage_count = usage_count + 1,
            updated_at = now()
        WHERE id = NEW.persona_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_conversation_created_persona ON conversations;
CREATE TRIGGER on_conversation_created_persona
    AFTER INSERT ON conversations
    FOR EACH ROW EXECUTE FUNCTION increment_persona_usage();
""")

    # 11. supabase/seed.sql
    create_file("supabase/seed.sql", """-- البيانات الأولية: 4 شخصيات نظامية مدمجة
-- كل شخصية لها وصف كامل ونص نظام عربي مفصل

-- ============================================
-- شخصية خبير لينكدإن
-- ============================================
INSERT INTO personas (id, user_id, name, description, system_prompt, icon_url, category, type, is_active, is_approved)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    NULL,
    'خبير لينكدإن',
    'متخصص في كتابة محتوى لينكدإن الاحترافي، تحسين الملفات الشخصية، وبناء العلامة التجارية الشخصية',
    'أنت خبير متخصص في منصة لينكدإن مع خبرة تزيد عن 10 سنوات في التسويق الرقمي والعلامات التجارية الشخصية. مهاراتك تشمل:

## تخصصاتك:
1. **كتابة المحتوى**: تكتب منشورات لينكدإن جذابة وفعالة تحقق تفاعلاً عالياً
2. **تحسين الملف الشخصي**: تساعد في كتابة العنوان الوظيفي، الملخص، وقسم الخبرات بشكل احترافي
3. **استراتيجية المحتوى**: تضع خطط محتوى أسبوعية وشهرية متكاملة
4. **بناء الشبكة المهنية**: تقدم نصائح لتوسيع شبكة العلاقات المهنية
5. **التفاعل والنمو**: تشارك أفضل الممارسات لزيادة المتابعين والتفاعل

## قواعدك:
- تكتب دائماً بأسلوب مهني لكن ودود
- تستخدم الرموز التعبيرية بشكل معتدل ومناسب
- تضع هاشتاقات مناسبة في نهاية كل منشور (3-5 هاشتاقات)
- تراعي خوارزمية لينكدإن في هيكلة المنشورات
- تبدأ كل منشور بجملة افتتاحية قوية تجذب القارئ (Hook)
- تستخدم الفقرات القصيرة والنقاط لسهولة القراءة
- تقدم قيمة حقيقية في كل منشور

## تنسيق الإجابة:
- قدم المنشور جاهزاً للنشر مباشرة
- أضف ملاحظات وتوجيهات بعد المنشور
- اقترح أفضل أوقات النشر إن أمكن
- قدم بدائل للعنوان أو الافتتاحية عند الطلب',
    '/persona-icons/linkedin.svg',
    'marketing',
    'system',
    true,
    true
);

-- ============================================
-- شخصية خبير العصف الذهني
-- ============================================
INSERT INTO personas (id, user_id, name, description, system_prompt, icon_url, category, type, is_active, is_approved)
VALUES (
    'a0000000-0000-0000-0000-000000000002',
    NULL,
    'خبير العصف الذهني',
    'متخصص في توليد الأفكار الإبداعية، حل المشكلات المعقدة، والتفكير خارج الصندوق',
    'أنت خبير في العصف الذهني والتفكير الإبداعي مع خبرة واسعة في ورش العمل الإبداعية وحل المشكلات. مهاراتك تشمل:

## تخصصاتك:
1. **توليد الأفكار**: تستخدم تقنيات متعددة لتوليد أفكار مبتكرة وغير تقليدية
2. **حل المشكلات**: تحلل المشكلات من زوايا مختلفة وتقدم حلولاً إبداعية
3. **تطوير المفاهيم**: تأخذ الأفكار الخام وتحولها لمفاهيم قابلة للتنفيذ
4. **التفكير التصميمي**: تطبق منهجية Design Thinking في حل المشكلات
5. **تحليل SWOT**: تقيم الأفكار من حيث نقاط القوة والضعف والفرص والتهديدات

## منهجيتك:
- تبدأ بفهم المشكلة أو الهدف بعمق قبل توليد الأفكار
- تطرح أسئلة توضيحية عند الحاجة
- تقدم الأفكار بشكل منظم مع تصنيفها حسب الجدوى والابتكار
- لا ترفض أي فكرة في مرحلة العصف الذهني
- تستخدم تقنيات مثل: SCAMPER، القبعات الست، الخريطة الذهنية

## تنسيق الإجابة:
- ابدأ بفهم السياق والهدف
- قدم الأفكار في مجموعات مصنفة
- رتب الأفكار من الأكثر تقليدية للأكثر إبداعاً
- أضف ملاحظات تنفيذية لكل فكرة
- اختم بتوصية لأفضل 3 أفكار مع التبرير
- استخدم الرموز 💡🎯🔥⭐ لتمييز مستوى الابتكار',
    '/persona-icons/brainstorm.svg',
    'general',
    'system',
    true,
    true
);

-- ============================================
-- شخصية خبير هندسة الأوامر
-- ============================================
INSERT INTO personas (id, user_id, name, description, system_prompt, icon_url, category, type, is_active, is_approved)
VALUES (
    'a0000000-0000-0000-0000-000000000003',
    NULL,
    'خبير هندسة الأوامر',
    'متخصص في كتابة وتحسين أوامر الذكاء الاصطناعي (Prompts) للحصول على أفضل النتائج',
    'أنت خبير في هندسة الأوامر (Prompt Engineering) مع فهم عميق لكيفية عمل نماذج اللغة الكبيرة. مهاراتك تشمل:

## تخصصاتك:
1. **كتابة الأوامر**: تكتب أوامر دقيقة ومفصلة تحقق النتائج المطلوبة
2. **تحسين الأوامر**: تحلل الأوامر الحالية وتحسنها لنتائج أفضل
3. **تقنيات متقدمة**: تتقن Chain-of-Thought، Few-Shot، Zero-Shot، Role-Playing
4. **أوامر النظام**: تصمم System Prompts احترافية للتطبيقات والبوتات
5. **اختبار وتقييم**: تقيم جودة الأوامر وتقترح تحسينات

## منهجيتك:
- تفهم الهدف النهائي قبل كتابة الأمر
- تستخدم هيكلة واضحة: السياق → المهمة → التنسيق → القيود
- تضيف أمثلة (Few-Shot) عندما يتطلب الأمر دقة عالية
- تحدد تنسيق الإخراج المطلوب بوضوح
- تتجنب الغموض وتستخدم تعليمات محددة

## أنماط الأوامر التي تتقنها:
- **CRISP**: Context, Role, Instructions, Specifics, Parameters
- **RACE**: Role, Action, Context, Expectations
- **CREATE**: Character, Request, Examples, Adjustments, Type, Extras
- **Chain-of-Thought**: تقسيم المهمة لخطوات تفكير متسلسلة

## تنسيق الإجابة:
- قدم الأمر المحسن في بلوك كود
- اشرح لماذا كل جزء مهم
- قدم نسخة عربية وإنجليزية إن طُلب
- أضف نصائح لتحسين النتائج
- اقترح متغيرات يمكن تعديلها حسب الحاجة',
    '/persona-icons/prompt.svg',
    'programming',
    'system',
    true,
    true
);

-- ============================================
-- شخصية خبير كتابة الإيميلات
-- ============================================
INSERT INTO personas (id, user_id, name, description, system_prompt, icon_url, category, type, is_active, is_approved)
VALUES (
    'a0000000-0000-0000-0000-000000000004',
    NULL,
    'خبير كتابة الإيميلات',
    'متخصص في كتابة رسائل البريد الإلكتروني الاحترافية بجميع أنواعها وأغراضها',
    'أنت خبير في كتابة رسائل البريد الإلكتروني الاحترافية مع خبرة في التواصل المؤسسي والتجاري. مهاراتك تشمل:

## تخصصاتك:
1. **رسائل العمل**: مراسلات رسمية، طلبات، متابعات، تقارير
2. **رسائل التسويق**: حملات بريدية، عروض، إعلانات منتجات
3. **رسائل التوظيف**: خطابات تقديم، متابعة مقابلات، عروض عمل
4. **رسائل العملاء**: دعم فني، شكاوى، اعتذارات، شكر
5. **رسائل الإدارة**: تعاميم، إعلانات داخلية، تقييمات

## قواعدك:
- تكتب بأسلوب مهني واضح ومباشر
- تراعي درجة الرسمية المناسبة للسياق
- تهيكل الرسالة: تحية → مقدمة → صلب الموضوع → خاتمة → توقيع
- تستخدم سطر موضوع جذاب ودقيق
- تتجنب الإطالة غير الضرورية
- تضيف دعوة لاتخاذ إجراء (CTA) واضحة
- تراعي الفروق الثقافية في المراسلات

## تنسيق الإجابة:
- **سطر الموضوع**: واضح ومحدد
- **نص الرسالة**: منسق وجاهز للإرسال
- **ملاحظات**: نصائح للإرسال والتوقيت
- **بدائل**: صيغ بديلة للنبرة (رسمية/ودية/حازمة)
- تقدم النسخة العربية والإنجليزية إن طُلب',
    '/persona-icons/email.svg',
    'writing',
    'system',
    true,
    true
);
""")

    # ──────────────────────────────────────────────
    # GROUP C: Utilities (6 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group C: Utility Files")
    print("-" * 40)

    # 12. app/globals.css
    create_file("app/globals.css", """/* الأنماط العامة: إعدادات Tailwind، شريط التمرير المخصص، ألوان التحديد */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --primary: #6c63ff;
    --secondary: #00d2ff;
    --accent: #f72585;
  }

  html {
    scroll-behavior: smooth;
  }

  body {
    @apply bg-white dark:bg-dark-950 text-gray-900 dark:text-gray-100;
    @apply font-sans antialiased;
  }

  [dir="rtl"] body {
    @apply font-sans-arabic;
  }

  ::selection {
    @apply bg-primary/30 text-primary-900 dark:text-primary-100;
  }

  ::-moz-selection {
    @apply bg-primary/30 text-primary-900 dark:text-primary-100;
  }
}

@layer components {
  /* شريط التمرير المخصص */
  .custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    @apply bg-transparent;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    @apply bg-gray-300 dark:bg-dark-600 rounded-full;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    @apply bg-gray-400 dark:bg-dark-500;
  }

  /* Firefox scrollbar */
  .custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: theme('colors.gray.300') transparent;
  }

  .dark .custom-scrollbar {
    scrollbar-color: theme('colors.dark.600') transparent;
  }

  /* مؤشر الكتابة الوامض */
  .typing-cursor::after {
    content: '▊';
    @apply text-primary animate-blink ml-0.5;
  }

  [dir="rtl"] .typing-cursor::after {
    @apply ml-0 mr-0.5;
  }

  /* تأثيرات الانتقال للشريط الجانبي */
  .sidebar-transition {
    @apply transition-all duration-300 ease-in-out;
  }

  /* تأثير التوهج للعناصر المحددة */
  .glow-primary {
    box-shadow: 0 0 15px theme('colors.primary.500 / 30%');
  }

  /* خلفية متدرجة للكروت */
  .gradient-card {
    @apply bg-gradient-to-br from-primary-500/10 to-secondary-500/10;
  }
}

@layer utilities {
  /* إخفاء شريط التمرير مع الحفاظ على وظيفة التمرير */
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  /* دعم اتجاه النص */
  .text-start {
    text-align: start;
  }

  .text-end {
    text-align: end;
  }
}
""")

    # 13. app/manifest.json
    create_file("app/manifest.json", """{
  "name": "AI Chat Platform",
  "short_name": "AI Chat",
  "description": "Professional Multi-Platform AI Chat Platform with Personas",
  "start_url": "/chat",
  "display": "standalone",
  "background_color": "#0f0f1a",
  "theme_color": "#6c63ff",
  "orientation": "any",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
""")

    # 14. utils/cn.ts
    create_file("utils/cn.ts", """// دالة مساعدة لدمج أسماء أصناف Tailwind CSS بذكاء باستخدام clsx و tailwind-merge
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * دمج أسماء الأصناف مع حل التعارضات في Tailwind
 * @param inputs - قائمة بأسماء الأصناف أو الشروط
 * @returns سلسلة أصناف مدمجة ومحسنة
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
""")

    # 15. utils/constants.ts
    create_file("utils/constants.ts", """// الثوابت العامة للتطبيق: حدود الاستخدام، المنصات المدعومة، أنواع الشخصيات والإشعارات

/**
 * حدود الاستخدام للحسابات المجانية والمميزة
 */
export const FREE_MESSAGES_BEFORE_DELAY = 4;
export const FREE_DELAY_SECONDS = 180;
export const PREMIUM_DELAY_SECONDS = 60;
export const MESSAGE_LIMIT_PER_CHAT = 15;
export const FREE_MAX_CONVERSATIONS = 20;
export const FREE_MAX_API_KEYS = 2;
export const FREE_MAX_PERSONAS = 4;
export const TRIAL_DURATION_DAYS = 3;

/**
 * معلومات المنصة الواحدة
 */
export interface PlatformInfo {
  readonly name: string;
  readonly displayName: string;
  readonly icon: string;
  readonly baseUrl: string;
  readonly authHeader: string;
  readonly isOpenAICompatible: boolean;
}

/**
 * المنصات المدعومة للذكاء الاصطناعي (7 منصات)
 */
export const SUPPORTED_PLATFORMS: readonly PlatformInfo[] = [
  {
    name: 'openrouter',
    displayName: 'OpenRouter',
    icon: '🌐',
    baseUrl: 'https://openrouter.ai/api/v1',
    authHeader: 'Authorization',
    isOpenAICompatible: true,
  },
  {
    name: 'groq',
    displayName: 'Groq',
    icon: '⚡',
    baseUrl: 'https://api.groq.com/openai/v1',
    authHeader: 'Authorization',
    isOpenAICompatible: true,
  },
  {
    name: 'openai',
    displayName: 'OpenAI',
    icon: '🤖',
    baseUrl: 'https://api.openai.com/v1',
    authHeader: 'Authorization',
    isOpenAICompatible: true,
  },
  {
    name: 'anthropic',
    displayName: 'Anthropic',
    icon: '🧠',
    baseUrl: 'https://api.anthropic.com/v1',
    authHeader: 'x-api-key',
    isOpenAICompatible: false,
  },
  {
    name: 'gemini',
    displayName: 'Google Gemini',
    icon: '💎',
    baseUrl: 'https://generativelanguage.googleapis.com/v1beta',
    authHeader: 'x-goog-api-key',
    isOpenAICompatible: false,
  },
  {
    name: 'together',
    displayName: 'Together AI',
    icon: '🤝',
    baseUrl: 'https://api.together.xyz/v1',
    authHeader: 'Authorization',
    isOpenAICompatible: true,
  },
  {
    name: 'mistral',
    displayName: 'Mistral',
    icon: '🌊',
    baseUrl: 'https://api.mistral.ai/v1',
    authHeader: 'Authorization',
    isOpenAICompatible: true,
  },
] as const;

/**
 * فئات الشخصيات
 */
export const PERSONA_CATEGORIES = [
  'writing',
  'marketing',
  'programming',
  'education',
  'translation',
  'general',
] as const;

/**
 * تصنيفات فئات الشخصيات مع التسميات
 */
export interface PersonaCategoryInfo {
  readonly value: string;
  readonly labelAr: string;
  readonly labelEn: string;
  readonly icon: string;
}

export const PERSONA_CATEGORY_INFO: readonly PersonaCategoryInfo[] = [
  { value: 'writing', labelAr: 'كتابة', labelEn: 'Writing', icon: '✍️' },
  { value: 'marketing', labelAr: 'تسويق', labelEn: 'Marketing', icon: '📢' },
  { value: 'programming', labelAr: 'برمجة', labelEn: 'Programming', icon: '💻' },
  { value: 'education', labelAr: 'تعليم', labelEn: 'Education', icon: '📚' },
  { value: 'translation', labelAr: 'ترجمة', labelEn: 'Translation', icon: '🌍' },
  { value: 'general', labelAr: 'عام', labelEn: 'General', icon: '🎯' },
] as const;

/**
 * أنواع الإشعارات التسعة
 */
export const NOTIFICATION_TYPES = [
  'user_registered',
  'trial_requested',
  'trial_expired',
  'premium_expired',
  'persona_shared',
  'api_low_balance',
  'api_depleted',
  'system_error',
  'invite_code_used',
] as const;

/**
 * معلومات أنواع الإشعارات
 */
export interface NotificationTypeInfo {
  readonly type: string;
  readonly labelAr: string;
  readonly labelEn: string;
  readonly icon: string;
  readonly defaultPriority: 'urgent' | 'normal' | 'info';
}

export const NOTIFICATION_TYPE_INFO: readonly NotificationTypeInfo[] = [
  { type: 'user_registered', labelAr: 'مستخدم جديد', labelEn: 'New User', icon: '👤', defaultPriority: 'info' },
  { type: 'trial_requested', labelAr: 'طلب تجربة', labelEn: 'Trial Requested', icon: '🎁', defaultPriority: 'normal' },
  { type: 'trial_expired', labelAr: 'انتهاء تجربة', labelEn: 'Trial Expired', icon: '⏰', defaultPriority: 'normal' },
  { type: 'premium_expired', labelAr: 'انتهاء اشتراك', labelEn: 'Premium Expired', icon: '💫', defaultPriority: 'normal' },
  { type: 'persona_shared', labelAr: 'شخصية مشتركة', labelEn: 'Persona Shared', icon: '🔄', defaultPriority: 'info' },
  { type: 'api_low_balance', labelAr: 'رصيد منخفض', labelEn: 'Low API Balance', icon: '⚠️', defaultPriority: 'urgent' },
  { type: 'api_depleted', labelAr: 'نفاد الرصيد', labelEn: 'API Depleted', icon: '🚫', defaultPriority: 'urgent' },
  { type: 'system_error', labelAr: 'خطأ نظام', labelEn: 'System Error', icon: '❌', defaultPriority: 'urgent' },
  { type: 'invite_code_used', labelAr: 'استخدام كود', labelEn: 'Invite Code Used', icon: '🎟️', defaultPriority: 'info' },
] as const;

/**
 * الأوامر المائلة للشخصيات المدمجة
 */
export interface SlashCommand {
  readonly command: string;
  readonly personaId: string;
  readonly labelAr: string;
  readonly labelEn: string;
  readonly description_ar: string;
  readonly description_en: string;
}

export const SLASH_COMMANDS: readonly SlashCommand[] = [
  {
    command: '/linkedin',
    personaId: 'a0000000-0000-0000-0000-000000000001',
    labelAr: 'خبير لينكدإن',
    labelEn: 'LinkedIn Expert',
    description_ar: 'كتابة محتوى لينكدإن احترافي',
    description_en: 'Write professional LinkedIn content',
  },
  {
    command: '/brainstorm',
    personaId: 'a0000000-0000-0000-0000-000000000002',
    labelAr: 'خبير العصف الذهني',
    labelEn: 'Brainstorming Expert',
    description_ar: 'توليد أفكار إبداعية وحل مشكلات',
    description_en: 'Generate creative ideas and solve problems',
  },
  {
    command: '/prompt',
    personaId: 'a0000000-0000-0000-0000-000000000003',
    labelAr: 'خبير هندسة الأوامر',
    labelEn: 'Prompt Engineering Expert',
    description_ar: 'كتابة وتحسين أوامر الذكاء الاصطناعي',
    description_en: 'Write and improve AI prompts',
  },
  {
    command: '/email',
    personaId: 'a0000000-0000-0000-0000-000000000004',
    labelAr: 'خبير كتابة الإيميلات',
    labelEn: 'Email Writing Expert',
    description_ar: 'كتابة رسائل بريد إلكتروني احترافية',
    description_en: 'Write professional emails',
  },
] as const;

/**
 * ثوابت واجهة المستخدم
 */
export const UI_CONSTANTS = {
  SIDEBAR_WIDTH: 280,
  HEADER_HEIGHT: 64,
  MAX_MESSAGE_LENGTH: 10000,
  MAX_PERSONA_NAME_LENGTH: 50,
  MAX_PERSONA_DESCRIPTION_LENGTH: 200,
  MAX_SYSTEM_PROMPT_LENGTH: 5000,
  MAX_CONVERSATION_TITLE_LENGTH: 100,
  MAX_FOLDER_NAME_LENGTH: 50,
  MAX_API_KEY_LABEL_LENGTH: 50,
  INVITE_CODE_LENGTH: 8,
  DEBOUNCE_DELAY: 300,
  TOAST_DURATION: 5000,
} as const;
""")

    # 16. utils/formatters.ts
    create_file("utils/formatters.ts", """// دوال التنسيق: التاريخ، الوقت النسبي، الأرقام، الرموز، المدة الزمنية

/**
 * تنسيق التاريخ حسب اللغة
 * @param date - التاريخ المراد تنسيقه
 * @param locale - اللغة (ar أو en)
 * @returns تاريخ منسق
 */
export function formatDate(date: Date | string, locale: string = 'ar'): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  if (isNaN(dateObj.getTime())) {
    return locale === 'ar' ? 'تاريخ غير صالح' : 'Invalid date';
  }

  const localeCode = locale === 'ar' ? 'ar-SA' : 'en-US';

  return new Intl.DateTimeFormat(localeCode, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(dateObj);
}

/**
 * تنسيق الوقت النسبي (منذ X دقيقة/ساعة/يوم)
 * @param date - التاريخ المراد حساب الفرق منه
 * @param locale - اللغة (ar أو en)
 * @returns وقت نسبي منسق
 */
export function formatRelativeTime(date: Date | string, locale: string = 'ar'): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  if (isNaN(dateObj.getTime())) {
    return locale === 'ar' ? 'تاريخ غير صالح' : 'Invalid date';
  }

  const now = new Date();
  const diffMs = now.getTime() - dateObj.getTime();
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  const diffWeeks = Math.floor(diffDays / 7);
  const diffMonths = Math.floor(diffDays / 30);

  if (locale === 'ar') {
    if (diffSecs < 60) return 'الآن';
    if (diffMins < 2) return 'منذ دقيقة';
    if (diffMins < 60) return `منذ ${diffMins} دقيقة`;
    if (diffHours < 2) return 'منذ ساعة';
    if (diffHours < 24) return `منذ ${diffHours} ساعة`;
    if (diffDays < 2) return 'أمس';
    if (diffDays < 7) return `منذ ${diffDays} أيام`;
    if (diffWeeks < 2) return 'منذ أسبوع';
    if (diffWeeks < 4) return `منذ ${diffWeeks} أسابيع`;
    if (diffMonths < 2) return 'منذ شهر';
    return `منذ ${diffMonths} أشهر`;
  }

  if (diffSecs < 60) return 'just now';
  if (diffMins < 2) return '1 minute ago';
  if (diffMins < 60) return `${diffMins} minutes ago`;
  if (diffHours < 2) return '1 hour ago';
  if (diffHours < 24) return `${diffHours} hours ago`;
  if (diffDays < 2) return 'yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffWeeks < 2) return '1 week ago';
  if (diffWeeks < 4) return `${diffWeeks} weeks ago`;
  if (diffMonths < 2) return '1 month ago';
  return `${diffMonths} months ago`;
}

/**
 * تنسيق الأرقام حسب اللغة (مع الفواصل)
 * @param num - الرقم المراد تنسيقه
 * @param locale - اللغة (ar أو en)
 * @returns رقم منسق
 */
export function formatNumber(num: number, locale: string = 'ar'): string {
  const localeCode = locale === 'ar' ? 'ar-SA' : 'en-US';
  return new Intl.NumberFormat(localeCode).format(num);
}

/**
 * تنسيق عدد الرموز (tokens) بشكل مختصر
 * @param tokens - عدد الرموز
 * @returns عدد رموز منسق (مثل 1.2K أو 3.5M)
 */
export function formatTokenCount(tokens: number): string {
  if (tokens < 1000) return tokens.toString();
  if (tokens < 1000000) return `${(tokens / 1000).toFixed(1)}K`;
  return `${(tokens / 1000000).toFixed(1)}M`;
}

/**
 * تنسيق المدة الزمنية بالثواني إلى نص مقروء
 * @param seconds - عدد الثواني
 * @returns مدة زمنية منسقة (مم:ثث)
 */
export function formatDuration(seconds: number): string {
  if (seconds < 0) return '00:00';

  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);

  const minsStr = mins.toString().padStart(2, '0');
  const secsStr = secs.toString().padStart(2, '0');

  return `${minsStr}:${secsStr}`;
}

/**
 * تنسيق حجم الملف
 * @param bytes - الحجم بالبايت
 * @returns حجم منسق (مثل 1.2 MB)
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';

  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  const size = bytes / Math.pow(1024, i);

  return `${size.toFixed(i === 0 ? 0 : 1)} ${sizes[i] ?? 'TB'}`;
}

/**
 * تنسيق وقت الاستجابة بالمللي ثانية
 * @param ms - الوقت بالمللي ثانية
 * @returns وقت منسق (مثل 1.2s أو 150ms)
 */
export function formatResponseTime(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}
""")

    # 17. utils/validators.ts
    create_file("utils/validators.ts", """// دوال التحقق: البريد الإلكتروني، كلمة المرور، مفاتيح API، أكواد الدعوة

/**
 * نتيجة التحقق من كلمة المرور
 */
export interface PasswordValidation {
  isValid: boolean;
  strength: 'weak' | 'medium' | 'strong';
  errors: string[];
}

/**
 * التحقق من صحة البريد الإلكتروني
 * @param email - البريد الإلكتروني
 * @returns هل البريد صالح؟
 */
export function isValidEmail(email: string): boolean {
  if (!email || typeof email !== 'string') return false;

  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email.trim());
}

/**
 * التحقق من قوة كلمة المرور
 * @param password - كلمة المرور
 * @returns نتيجة التحقق مع مستوى القوة والأخطاء
 */
export function isValidPassword(password: string): PasswordValidation {
  const errors: string[] = [];

  if (!password || typeof password !== 'string') {
    return { isValid: false, strength: 'weak', errors: ['Password is required'] };
  }

  if (password.length < 8) {
    errors.push('min_length');
  }

  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecial = /[!@#$%^&*()_+\\-=\\[\\]{};':"\\\\|,.<>\\/?]/.test(password);

  if (!hasUppercase && !hasLowercase) {
    errors.push('need_letter');
  }

  if (!hasNumber) {
    errors.push('need_number');
  }

  let strengthScore = 0;
  if (password.length >= 8) strengthScore++;
  if (password.length >= 12) strengthScore++;
  if (hasUppercase) strengthScore++;
  if (hasLowercase) strengthScore++;
  if (hasNumber) strengthScore++;
  if (hasSpecial) strengthScore++;

  let strength: 'weak' | 'medium' | 'strong';
  if (strengthScore <= 2) {
    strength = 'weak';
  } else if (strengthScore <= 4) {
    strength = 'medium';
  } else {
    strength = 'strong';
  }

  return {
    isValid: password.length >= 8 && errors.length === 0,
    strength,
    errors,
  };
}

/**
 * التحقق من صحة مفتاح API حسب المنصة
 * @param key - مفتاح API
 * @param platform - اسم المنصة
 * @returns هل المفتاح يتوافق مع تنسيق المنصة؟
 */
export function isValidApiKey(key: string, platform: string): boolean {
  if (!key || typeof key !== 'string' || key.trim().length === 0) {
    return false;
  }

  const trimmedKey = key.trim();

  switch (platform) {
    case 'openrouter':
      return trimmedKey.startsWith('sk-or-') && trimmedKey.length > 10;

    case 'groq':
      return trimmedKey.startsWith('gsk_') && trimmedKey.length > 10;

    case 'openai':
      return trimmedKey.startsWith('sk-') && trimmedKey.length > 10;

    case 'anthropic':
      return trimmedKey.startsWith('sk-ant-') && trimmedKey.length > 10;

    case 'gemini':
      return trimmedKey.startsWith('AI') && trimmedKey.length > 10;

    case 'together':
      return trimmedKey.length > 10;

    case 'mistral':
      return trimmedKey.length > 10;

    default:
      return trimmedKey.length > 5;
  }
}

/**
 * التحقق من صحة كود الدعوة
 * @param code - كود الدعوة
 * @returns هل الكود يحتوي على أحرف وأرقام فقط؟
 */
export function isValidInviteCode(code: string): boolean {
  if (!code || typeof code !== 'string') return false;

  const alphanumericRegex = /^[a-zA-Z0-9]+$/;
  return alphanumericRegex.test(code.trim()) && code.trim().length >= 4;
}

/**
 * التحقق من صحة اسم العرض
 * @param name - الاسم
 * @returns هل الاسم صالح؟
 */
export function isValidDisplayName(name: string): boolean {
  if (!name || typeof name !== 'string') return false;

  const trimmed = name.trim();
  return trimmed.length >= 2 && trimmed.length <= 50;
}

/**
 * التحقق من صحة نص النظام (System Prompt)
 * @param prompt - نص النظام
 * @returns هل النص صالح؟
 */
export function isValidSystemPrompt(prompt: string): boolean {
  if (!prompt || typeof prompt !== 'string') return false;

  const trimmed = prompt.trim();
  return trimmed.length >= 10 && trimmed.length <= 5000;
}

/**
 * تنقية النص من الأحرف الخطرة
 * @param input - النص المدخل
 * @returns نص منقى
 */
export function sanitizeInput(input: string): string {
  if (!input || typeof input !== 'string') return '';

  return input
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .trim();
}
""")

    # 18. utils/helpers.ts
    create_file("utils/helpers.ts", """// دوال مساعدة عامة: توليد أكواد، اقتصاص نص، أحرف أولى، تأخير، اتجاه اللغة

/**
 * توليد كود عشوائي من أحرف وأرقام
 * @param length - طول الكود (افتراضي 8)
 * @returns كود عشوائي
 */
export function generateRandomCode(length: number = 8): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';

  const array = new Uint8Array(length);
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    crypto.getRandomValues(array);
  } else {
    for (let i = 0; i < length; i++) {
      array[i] = Math.floor(Math.random() * 256);
    }
  }

  for (let i = 0; i < length; i++) {
    const index = array[i];
    if (index !== undefined) {
      result += chars[index % chars.length];
    }
  }

  return result;
}

/**
 * اقتصاص النص مع إضافة علامة الحذف
 * @param text - النص الأصلي
 * @param max - الحد الأقصى للأحرف (افتراضي 50)
 * @returns نص مقتصر
 */
export function truncateText(text: string, max: number = 50): string {
  if (!text || typeof text !== 'string') return '';

  if (text.length <= max) return text;

  return text.substring(0, max).trim() + '...';
}

/**
 * استخراج الأحرف الأولى من الاسم
 * @param name - الاسم الكامل
 * @returns حرف أو حرفين أوليين
 */
export function getInitials(name: string): string {
  if (!name || typeof name !== 'string') return '?';

  const trimmed = name.trim();
  if (trimmed.length === 0) return '?';

  const words = trimmed.split(/\\s+/);

  if (words.length === 1) {
    const firstWord = words[0];
    return firstWord ? firstWord.substring(0, 2).toUpperCase() : '?';
  }

  const first = words[0];
  const last = words[words.length - 1];

  const firstChar = first ? first[0] : '';
  const lastChar = last ? last[0] : '';

  return (firstChar + lastChar).toUpperCase();
}

/**
 * تأخير تنفيذ الدالة (Debounce)
 * @param fn - الدالة المراد تأخيرها
 * @param delay - مدة التأخير بالمللي ثانية (افتراضي 300)
 * @returns دالة مؤجلة
 */
export function debounce<T extends (...args: Parameters<T>) => ReturnType<T>>(
  fn: T,
  delay: number = 300
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  return (...args: Parameters<T>) => {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      fn(...args);
      timeoutId = null;
    }, delay);
  };
}

/**
 * تأخير بالمللي ثانية (Promise-based)
 * @param ms - المدة بالمللي ثانية
 * @returns Promise ينتهي بعد المدة المحددة
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

/**
 * تحديد اتجاه النص بناءً على اللغة
 * @param locale - كود اللغة (ar أو en)
 * @returns اتجاه النص (rtl أو ltr)
 */
export function getDirectionFromLocale(locale: string): 'rtl' | 'ltr' {
  return locale === 'ar' ? 'rtl' : 'ltr';
}

/**
 * التحقق مما إذا كان المتصفح يدعم خاصية معينة
 * @param feature - اسم الخاصية
 * @returns هل الخاصية مدعومة؟
 */
export function isFeatureSupported(feature: 'clipboard' | 'share' | 'notification'): boolean {
  if (typeof window === 'undefined') return false;

  switch (feature) {
    case 'clipboard':
      return Boolean(navigator.clipboard);
    case 'share':
      return Boolean(navigator.share);
    case 'notification':
      return 'Notification' in window;
    default:
      return false;
  }
}

/**
 * نسخ نص إلى الحافظة
 * @param text - النص المراد نسخه
 * @returns هل تمت العملية بنجاح؟
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text);
      return true;
    }

    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    const result = document.execCommand('copy');
    document.body.removeChild(textarea);
    return result;
  } catch {
    return false;
  }
}

/**
 * تحويل سلسلة UUID صالحة
 * @param id - النص المراد التحقق منه
 * @returns هل هو UUID صالح؟
 */
export function isValidUUID(id: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(id);
}
""")

    # ──────────────────────────────────────────────
    # GROUP D: TypeScript Types (9 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group D: TypeScript Type Files")
    print("-" * 40)

    # 19. types/user.ts
    create_file("types/user.ts", """// أنواع المستخدم: الأدوار، الملف الشخصي، حالة المصادقة

/**
 * أدوار المستخدمين في النظام
 */
export type Role = 'admin' | 'premium' | 'free';

/**
 * الملف الشخصي للمستخدم - يطابق جدول profiles
 */
export interface Profile {
  id: string;
  email: string;
  display_name: string | null;
  role: Role;
  is_super_admin: boolean;
  premium_expires_at: string | null;
  trial_used: boolean;
  trial_expires_at: string | null;
  is_banned: boolean;
  onboarding_completed: boolean;
  preferred_language: string;
  preferred_theme: string;
  created_at: string;
  updated_at: string;
}

/**
 * حالة المصادقة في التطبيق
 */
export interface AuthState {
  user: Profile | null;
  role: Role;
  isLoading: boolean;
  isBanned: boolean;
  isSuperAdmin: boolean;
  trialUsed: boolean;
}

/**
 * بيانات تحديث الملف الشخصي
 */
export interface ProfileUpdateData {
  display_name?: string;
  preferred_language?: string;
  preferred_theme?: string;
  onboarding_completed?: boolean;
}

/**
 * بيانات تحديث المستخدم من قبل المدير
 */
export interface AdminUserUpdateData {
  role?: Role;
  is_banned?: boolean;
  premium_expires_at?: string | null;
  trial_used?: boolean;
  trial_expires_at?: string | null;
}

/**
 * إحصائيات المستخدم
 */
export interface UserStats {
  totalConversations: number;
  totalMessages: number;
  totalTokens: number;
  totalPersonas: number;
  totalApiKeys: number;
}
""")

    # 20. types/chat.ts
    create_file("types/chat.ts", """// أنواع الدردشة: أدوار الرسائل، الرسائل، المحادثات، حالة البث

/**
 * أدوار الرسائل في المحادثة
 */
export type MessageRole = 'user' | 'assistant' | 'system';

/**
 * الرسالة - تطابق جدول messages
 */
export interface Message {
  id: string;
  conversation_id: string;
  role: MessageRole;
  content: string;
  model: string | null;
  platform: string | null;
  persona_name: string | null;
  tokens_used: number;
  response_time_ms: number | null;
  created_at: string;
}

/**
 * المحادثة - تطابق جدول conversations
 */
export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  persona_id: string | null;
  platform: string;
  model: string;
  folder_id: string | null;
  is_favorited: boolean;
  message_count: number;
  total_tokens: number;
  created_at: string;
  updated_at: string;
}

/**
 * حالة البث المباشر
 */
export interface StreamState {
  isStreaming: boolean;
  isSending: boolean;
}

/**
 * بيانات إنشاء رسالة جديدة
 */
export interface CreateMessageData {
  conversation_id: string;
  role: MessageRole;
  content: string;
  model?: string;
  platform?: string;
  persona_name?: string;
  tokens_used?: number;
  response_time_ms?: number;
}

/**
 * بيانات إنشاء محادثة جديدة
 */
export interface CreateConversationData {
  title?: string;
  persona_id?: string | null;
  platform: string;
  model: string;
  folder_id?: string | null;
}

/**
 * بيانات تحديث المحادثة
 */
export interface UpdateConversationData {
  title?: string;
  folder_id?: string | null;
  is_favorited?: boolean;
}

/**
 * رسالة للإرسال إلى مزود الذكاء الاصطناعي
 */
export interface AIMessage {
  role: MessageRole;
  content: string;
}

/**
 * طلب الدردشة للـ API
 */
export interface ChatRequest {
  messages: AIMessage[];
  model: string;
  platform: string;
  conversationId: string;
  personaName?: string;
  apiKeyId?: string;
  isGlobalKey?: boolean;
}

/**
 * استجابة الدردشة من الـ API
 */
export interface ChatResponse {
  content: string;
  tokensUsed: number;
  responseTimeMs: number;
}
""")

    # 21. types/persona.ts
    create_file("types/persona.ts", """// أنواع الشخصيات: أنواع الشخصية، الفئات، التقييمات

/**
 * أنواع الشخصيات في النظام
 */
export type PersonaType = 'system' | 'premium' | 'custom' | 'shared';

/**
 * فئات الشخصيات
 */
export type PersonaCategory = 'writing' | 'marketing' | 'programming' | 'education' | 'translation' | 'general';

/**
 * الشخصية - تطابق جدول personas
 */
export interface Persona {
  id: string;
  user_id: string | null;
  name: string;
  description: string;
  system_prompt: string;
  icon_url: string | null;
  category: PersonaCategory;
  type: PersonaType;
  is_active: boolean;
  is_approved: boolean;
  average_rating: number;
  rating_count: number;
  usage_count: number;
  created_at: string;
  updated_at: string;
}

/**
 * تقييم الشخصية - تطابق جدول persona_ratings
 */
export interface PersonaRating {
  id: string;
  persona_id: string;
  user_id: string;
  rating: number;
  created_at: string;
}

/**
 * بيانات إنشاء شخصية جديدة
 */
export interface CreatePersonaData {
  name: string;
  description: string;
  system_prompt: string;
  icon_url?: string;
  category: PersonaCategory;
  type: PersonaType;
}

/**
 * بيانات تحديث الشخصية
 */
export interface UpdatePersonaData {
  name?: string;
  description?: string;
  system_prompt?: string;
  icon_url?: string;
  category?: PersonaCategory;
  is_active?: boolean;
  is_approved?: boolean;
}

/**
 * تجربة الشخصية المميزة - تطابق جدول premium_persona_trials
 */
export interface PremiumPersonaTrial {
  id: string;
  user_id: string;
  persona_id: string;
  used_at: string;
}

/**
 * الشخصية مع معلومات إضافية للعرض
 */
export interface PersonaWithMeta extends Persona {
  userRating?: number;
  hasTrialUsed?: boolean;
  isLocked?: boolean;
}
""")

    # 22. types/platform.ts
    create_file("types/platform.ts", """// أنواع المنصات: أسماء المنصات، النماذج، مزودي الذكاء الاصطناعي، إعدادات المزود

import type { AIMessage } from './chat';

/**
 * أسماء المنصات المدعومة
 */
export type PlatformName =
  | 'openrouter'
  | 'groq'
  | 'openai'
  | 'anthropic'
  | 'gemini'
  | 'together'
  | 'mistral';

/**
 * معلومات المنصة
 */
export interface Platform {
  name: PlatformName;
  displayName: string;
  icon: string;
  baseUrl: string;
  authMethod: 'bearer' | 'api-key' | 'query';
}

/**
 * النموذج (Model) للذكاء الاصطناعي
 */
export interface Model {
  id: string;
  name: string;
  description?: string;
}

/**
 * واجهة مزود الذكاء الاصطناعي
 */
export interface AIProvider {
  sendMessage: (config: ProviderRequestConfig) => Promise<ReadableStream<Uint8Array>>;
  fetchModels: (apiKey: string) => Promise<Model[]>;
}

/**
 * إعدادات المزود
 */
export interface ProviderConfig {
  baseUrl: string;
  authHeader: string;
  streamPath: string;
}

/**
 * إعدادات طلب المزود
 */
export interface ProviderRequestConfig {
  apiKey: string;
  model: string;
  messages: AIMessage[];
  stream?: boolean;
  maxTokens?: number;
  temperature?: number;
}

/**
 * استجابة البث (Streaming Response chunk)
 */
export interface StreamChunk {
  content: string;
  isFinished: boolean;
  tokensUsed?: number;
}

/**
 * النموذج المعروض في واجهة المستخدم
 */
export interface DisplayModel {
  id: string;
  name: string;
  platform: PlatformName;
  isGlobal: boolean;
  apiKeyId: string;
}

/**
 * حالة اختيار المنصة والنموذج
 */
export interface PlatformSelection {
  platform: PlatformName;
  model: string;
  apiKeyId: string;
  isGlobalKey: boolean;
}
""")

    # 23. types/api-key.ts
    create_file("types/api-key.ts", """// أنواع مفاتيح API: المفتاح، النموذج العام

/**
 * مفتاح API - يطابق جدول api_keys
 */
export interface ApiKey {
  id: string;
  user_id: string | null;
  platform: string;
  encrypted_key: string;
  label: string;
  is_global: boolean;
  is_active: boolean;
  last_used_at: string | null;
  created_at: string;
}

/**
 * النموذج العام - يطابق جدول global_models
 */
export interface GlobalModel {
  id: string;
  api_key_id: string;
  model_id: string;
  model_name: string;
  is_active: boolean;
  sort_order: number;
  created_at: string;
}

/**
 * بيانات إنشاء مفتاح API جديد
 */
export interface CreateApiKeyData {
  platform: string;
  key: string;
  label: string;
  is_global?: boolean;
}

/**
 * بيانات تحديث مفتاح API
 */
export interface UpdateApiKeyData {
  label?: string;
  is_active?: boolean;
}

/**
 * بيانات إنشاء نموذج عام
 */
export interface CreateGlobalModelData {
  api_key_id: string;
  model_id: string;
  model_name: string;
  sort_order?: number;
}

/**
 * مفتاح API مع النماذج المرتبطة
 */
export interface ApiKeyWithModels extends ApiKey {
  global_models?: GlobalModel[];
}

/**
 * مفتاح API مفكك التشفير (للاستخدام الداخلي فقط)
 */
export interface DecryptedApiKey {
  id: string;
  platform: string;
  decryptedKey: string;
  label: string;
  isGlobal: boolean;
}
""")

    # 24. types/folder.ts
    create_file("types/folder.ts", """// أنواع المجلدات: نوع المجلد، المجلد مع المحادثات

/**
 * أنواع المجلدات
 */
export type FolderType = 'auto' | 'custom';

/**
 * المجلد - يطابق جدول folders
 */
export interface Folder {
  id: string;
  user_id: string;
  name: string;
  type: FolderType;
  persona_id: string | null;
  sort_order: number;
  created_at: string;
}

/**
 * بيانات إنشاء مجلد جديد
 */
export interface CreateFolderData {
  name: string;
  type: FolderType;
  persona_id?: string;
  sort_order?: number;
}

/**
 * بيانات تحديث المجلد
 */
export interface UpdateFolderData {
  name?: string;
  sort_order?: number;
}

/**
 * المجلد مع عدد المحادثات
 */
export interface FolderWithCount extends Folder {
  conversation_count: number;
}
""")

    # 25. types/notification.ts
    create_file("types/notification.ts", """// أنواع الإشعارات: أنواع الإشعار، الأولوية، الإشعار الكامل

/**
 * أنواع الإشعارات التسعة
 */
export type NotificationType =
  | 'user_registered'
  | 'trial_requested'
  | 'trial_expired'
  | 'premium_expired'
  | 'persona_shared'
  | 'api_low_balance'
  | 'api_depleted'
  | 'system_error'
  | 'invite_code_used';

/**
 * أولويات الإشعارات
 */
export type NotificationPriority = 'urgent' | 'normal' | 'info';

/**
 * الإشعار - يطابق جدول notifications
 */
export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  priority: NotificationPriority;
  is_read: boolean;
  related_user_id: string | null;
  metadata: Record<string, unknown> | null;
  created_at: string;
}

/**
 * بيانات إنشاء إشعار جديد
 */
export interface CreateNotificationData {
  type: NotificationType;
  title: string;
  message: string;
  priority?: NotificationPriority;
  related_user_id?: string;
  metadata?: Record<string, unknown>;
}

/**
 * فلتر الإشعارات
 */
export interface NotificationFilter {
  type?: NotificationType;
  priority?: NotificationPriority;
  isRead?: boolean;
  limit?: number;
  offset?: number;
}
""")

    # 26. types/invite-code.ts
    create_file("types/invite-code.ts", """// أنواع أكواد الدعوة: الكود، سجل الاستخدام

/**
 * كود الدعوة - يطابق جدول invite_codes
 */
export interface InviteCode {
  id: string;
  code: string;
  created_by: string;
  max_uses: number;
  current_uses: number;
  premium_duration_days: number | null;
  is_active: boolean;
  expires_at: string | null;
  created_at: string;
}

/**
 * سجل استخدام كود الدعوة - يطابق جدول invite_code_uses
 */
export interface InviteCodeUse {
  id: string;
  invite_code_id: string;
  user_id: string;
  used_at: string;
}

/**
 * بيانات إنشاء كود دعوة جديد
 */
export interface CreateInviteCodeData {
  code?: string;
  max_uses?: number;
  premium_duration_days?: number;
  expires_at?: string;
}

/**
 * بيانات تحديث كود الدعوة
 */
export interface UpdateInviteCodeData {
  is_active?: boolean;
  max_uses?: number;
  expires_at?: string | null;
}

/**
 * كود الدعوة مع معلومات المنشئ
 */
export interface InviteCodeWithCreator extends InviteCode {
  creator_email?: string;
  creator_name?: string;
}

/**
 * سجل استخدام مع معلومات المستخدم
 */
export interface InviteCodeUseWithUser extends InviteCodeUse {
  user_email?: string;
  user_name?: string;
}
""")

    # ──────────────────────────────────────────────
    # Create necessary directories for public assets
    # ──────────────────────────────────────────────
    print("\n📁 Creating Public Directories")
    print("-" * 40)

    # public/robots.txt
    create_file("public/robots.txt", """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Sitemap: https://your-domain.pages.dev/sitemap.xml
""")

    # Create placeholder icon directories
    os.makedirs("public/icons", exist_ok=True)
    print("  📂 Created: public/icons/")
    os.makedirs("public/persona-icons", exist_ok=True)
    print("  📂 Created: public/persona-icons/")

    # postcss.config.js (required for Tailwind)
    create_file("postcss.config.js", """// إعدادات PostCSS مع Tailwind CSS و Autoprefixer
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
""")

    # i18n/config.ts placeholder (needed by next.config.js)
    create_file("i18n/config.ts", """// إعدادات التدويل (i18n) - next-intl
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => {
  const validLocale = locale === 'en' ? 'en' : 'ar';

  return {
    messages: (await import(\`@/i18n/\${validLocale}.json\`)).default,
  };
});
""")

    # Minimal i18n files to prevent build errors
    create_file("i18n/ar.json", """{
  "common": {
    "appName": "منصة الدردشة بالذكاء الاصطناعي",
    "loading": "جاري التحميل...",
    "error": "حدث خطأ",
    "save": "حفظ",
    "cancel": "إلغاء",
    "delete": "حذف",
    "edit": "تعديل",
    "create": "إنشاء",
    "search": "بحث",
    "confirm": "تأكيد",
    "back": "رجوع",
    "next": "التالي",
    "previous": "السابق",
    "close": "إغلاق",
    "copy": "نسخ",
    "copied": "تم النسخ",
    "yes": "نعم",
    "no": "لا",
    "or": "أو",
    "and": "و",
    "all": "الكل",
    "none": "لا شيء",
    "required": "مطلوب",
    "optional": "اختياري",
    "success": "تمت العملية بنجاح",
    "noResults": "لا توجد نتائج",
    "tryAgain": "حاول مرة أخرى"
  },
  "auth": {
    "login": "تسجيل الدخول",
    "register": "إنشاء حساب",
    "logout": "تسجيل الخروج",
    "email": "البريد الإلكتروني",
    "password": "كلمة المرور",
    "confirmPassword": "تأكيد كلمة المرور",
    "displayName": "الاسم المعروض",
    "loginTitle": "مرحباً بعودتك",
    "registerTitle": "إنشاء حساب جديد",
    "noAccount": "ليس لديك حساب؟",
    "hasAccount": "لديك حساب بالفعل؟",
    "loginError": "خطأ في تسجيل الدخول",
    "registerError": "خطأ في إنشاء الحساب",
    "invalidCredentials": "البريد الإلكتروني أو كلمة المرور غير صحيحة",
    "emailRequired": "البريد الإلكتروني مطلوب",
    "passwordRequired": "كلمة المرور مطلوبة",
    "passwordMinLength": "كلمة المرور يجب أن تكون 8 أحرف على الأقل",
    "passwordMismatch": "كلمات المرور غير متطابقة",
    "banned": "تم حظر حسابك"
  },
  "chat": {
    "newChat": "محادثة جديدة",
    "sendMessage": "إرسال رسالة",
    "typeMessage": "اكتب رسالتك...",
    "thinking": "يفكر...",
    "streaming": "يكتب...",
    "messageLimit": "وصلت للحد الأقصى للرسائل في هذه المحادثة",
    "rateLimitWait": "يرجى الانتظار قبل إرسال رسالة أخرى",
    "freeMessagesLeft": "رسائل مجانية متبقية",
    "selectModel": "اختر نموذجاً",
    "selectPlatform": "اختر منصة",
    "noConversations": "لا توجد محادثات بعد",
    "startChatting": "ابدأ محادثة جديدة",
    "deleteConversation": "حذف المحادثة",
    "deleteConfirm": "هل أنت متأكد من حذف هذه المحادثة؟",
    "renameConversation": "إعادة تسمية المحادثة",
    "exportChat": "تصدير المحادثة",
    "copyMessage": "نسخ الرسالة",
    "regenerate": "إعادة التوليد",
    "stop": "إيقاف",
    "tokens": "رموز",
    "responseTime": "وقت الاستجابة"
  },
  "personas": {
    "title": "الشخصيات",
    "myPersonas": "شخصياتي",
    "systemPersonas": "شخصيات النظام",
    "premiumPersonas": "شخصيات مميزة",
    "sharedPersonas": "شخصيات مشتركة",
    "createPersona": "إنشاء شخصية",
    "editPersona": "تعديل الشخصية",
    "deletePersona": "حذف الشخصية",
    "personaName": "اسم الشخصية",
    "personaDescription": "وصف الشخصية",
    "systemPrompt": "نص النظام",
    "category": "الفئة",
    "rating": "التقييم",
    "usageCount": "مرات الاستخدام",
    "trialMessage": "رسالة تجريبية واحدة",
    "trialUsed": "تم استخدام التجربة",
    "locked": "مقفلة - للمشتركين فقط",
    "sharePersona": "مشاركة الشخصية",
    "pendingApproval": "في انتظار الموافقة",
    "approved": "معتمدة",
    "limitReached": "وصلت للحد الأقصى من الشخصيات المخصصة"
  },
  "settings": {
    "title": "الإعدادات",
    "profile": "الملف الشخصي",
    "apiKeys": "مفاتيح API",
    "language": "اللغة",
    "theme": "المظهر",
    "darkMode": "الوضع المظلم",
    "lightMode": "الوضع الفاتح",
    "arabic": "العربية",
    "english": "الإنجليزية",
    "addApiKey": "إضافة مفتاح API",
    "deleteApiKey": "حذف المفتاح",
    "platform": "المنصة",
    "keyLabel": "تسمية المفتاح",
    "apiKey": "مفتاح API",
    "exportData": "تصدير البيانات",
    "importData": "استيراد البيانات",
    "trial": "الفترة التجريبية",
    "startTrial": "بدء التجربة المجانية",
    "trialActive": "التجربة نشطة",
    "trialExpired": "انتهت التجربة",
    "trialDays": "3 أيام مجاناً",
    "premium": "مميز",
    "free": "مجاني",
    "admin": "مدير"
  },
  "admin": {
    "title": "لوحة الإدارة",
    "dashboard": "لوحة المعلومات",
    "users": "المستخدمون",
    "apiKeys": "مفاتيح API",
    "models": "النماذج",
    "personas": "الشخصيات",
    "sharedPersonas": "الشخصيات المشتركة",
    "inviteCodes": "أكواد الدعوة",
    "notifications": "الإشعارات",
    "settings": "الإعدادات",
    "totalUsers": "إجمالي المستخدمين",
    "premiumUsers": "المستخدمون المميزون",
    "totalConversations": "إجمالي المحادثات",
    "totalMessages": "إجمالي الرسائل",
    "banUser": "حظر المستخدم",
    "unbanUser": "إلغاء الحظر",
    "upgradeUser": "ترقية للمميز",
    "downgradeUser": "تخفيض للمجاني",
    "makeAdmin": "جعله مديراً",
    "removeAdmin": "إزالة الإدارة",
    "createInviteCode": "إنشاء كود دعوة",
    "approvePersona": "الموافقة على الشخصية",
    "rejectPersona": "رفض الشخصية"
  },
  "errors": {
    "generic": "حدث خطأ غير متوقع",
    "network": "خطأ في الاتصال بالشبكة",
    "unauthorized": "غير مصرح لك بالوصول",
    "notFound": "الصفحة غير موجودة",
    "rateLimited": "تم تجاوز حد الطلبات",
    "serverError": "خطأ في الخادم",
    "invalidInput": "البيانات المدخلة غير صالحة",
    "limitReached": "وصلت للحد الأقصى المسموح",
    "apiKeyInvalid": "مفتاح API غير صالح",
    "modelNotFound": "النموذج غير موجود"
  },
  "onboarding": {
    "welcome": "مرحباً بك!",
    "step1Title": "الشريط الجانبي",
    "step1Description": "هنا تجد محادثاتك ومجلداتك ومفضلاتك",
    "step2Title": "الشريط العلوي",
    "step2Description": "اختر المنصة والنموذج والشخصية من هنا",
    "step3Title": "الشخصيات",
    "step3Description": "استخدم شخصيات جاهزة أو أنشئ شخصياتك الخاصة",
    "step4Title": "الاختصارات",
    "step4Description": "اكتب / للوصول السريع للشخصيات المدمجة",
    "step5Title": "الإعدادات ومفاتيح API",
    "step5Description": "أضف مفاتيح API الخاصة بك للوصول المباشر للنماذج",
    "step6Title": "ابدأ الآن!",
    "step6Description": "أنت جاهز لبدء المحادثة مع الذكاء الاصطناعي",
    "skip": "تخطي",
    "finish": "ابدأ الاستخدام"
  }
}
""")

    create_file("i18n/en.json", """{
  "common": {
    "appName": "AI Chat Platform",
    "loading": "Loading...",
    "error": "An error occurred",
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "create": "Create",
    "search": "Search",
    "confirm": "Confirm",
    "back": "Back",
    "next": "Next",
    "previous": "Previous",
    "close": "Close",
    "copy": "Copy",
    "copied": "Copied",
    "yes": "Yes",
    "no": "No",
    "or": "or",
    "and": "and",
    "all": "All",
    "none": "None",
    "required": "Required",
    "optional": "Optional",
    "success": "Operation completed successfully",
    "noResults": "No results found",
    "tryAgain": "Try again"
  },
  "auth": {
    "login": "Login",
    "register": "Register",
    "logout": "Logout",
    "email": "Email",
    "password": "Password",
    "confirmPassword": "Confirm Password",
    "displayName": "Display Name",
    "loginTitle": "Welcome Back",
    "registerTitle": "Create New Account",
    "noAccount": "Don't have an account?",
    "hasAccount": "Already have an account?",
    "loginError": "Login error",
    "registerError": "Registration error",
    "invalidCredentials": "Invalid email or password",
    "emailRequired": "Email is required",
    "passwordRequired": "Password is required",
    "passwordMinLength": "Password must be at least 8 characters",
    "passwordMismatch": "Passwords do not match",
    "banned": "Your account has been banned"
  },
  "chat": {
    "newChat": "New Chat",
    "sendMessage": "Send Message",
    "typeMessage": "Type your message...",
    "thinking": "Thinking...",
    "streaming": "Typing...",
    "messageLimit": "You've reached the message limit for this conversation",
    "rateLimitWait": "Please wait before sending another message",
    "freeMessagesLeft": "free messages left",
    "selectModel": "Select a model",
    "selectPlatform": "Select a platform",
    "noConversations": "No conversations yet",
    "startChatting": "Start a new conversation",
    "deleteConversation": "Delete conversation",
    "deleteConfirm": "Are you sure you want to delete this conversation?",
    "renameConversation": "Rename conversation",
    "exportChat": "Export chat",
    "copyMessage": "Copy message",
    "regenerate": "Regenerate",
    "stop": "Stop",
    "tokens": "tokens",
    "responseTime": "Response time"
  },
  "personas": {
    "title": "Personas",
    "myPersonas": "My Personas",
    "systemPersonas": "System Personas",
    "premiumPersonas": "Premium Personas",
    "sharedPersonas": "Shared Personas",
    "createPersona": "Create Persona",
    "editPersona": "Edit Persona",
    "deletePersona": "Delete Persona",
    "personaName": "Persona Name",
    "personaDescription": "Persona Description",
    "systemPrompt": "System Prompt",
    "category": "Category",
    "rating": "Rating",
    "usageCount": "Usage Count",
    "trialMessage": "One trial message",
    "trialUsed": "Trial used",
    "locked": "Locked - Premium only",
    "sharePersona": "Share Persona",
    "pendingApproval": "Pending approval",
    "approved": "Approved",
    "limitReached": "Custom persona limit reached"
  },
  "settings": {
    "title": "Settings",
    "profile": "Profile",
    "apiKeys": "API Keys",
    "language": "Language",
    "theme": "Theme",
    "darkMode": "Dark Mode",
    "lightMode": "Light Mode",
    "arabic": "Arabic",
    "english": "English",
    "addApiKey": "Add API Key",
    "deleteApiKey": "Delete Key",
    "platform": "Platform",
    "keyLabel": "Key Label",
    "apiKey": "API Key",
    "exportData": "Export Data",
    "importData": "Import Data",
    "trial": "Trial",
    "startTrial": "Start Free Trial",
    "trialActive": "Trial Active",
    "trialExpired": "Trial Expired",
    "trialDays": "3 days free",
    "premium": "Premium",
    "free": "Free",
    "admin": "Admin"
  },
  "admin": {
    "title": "Admin Panel",
    "dashboard": "Dashboard",
    "users": "Users",
    "apiKeys": "API Keys",
    "models": "Models",
    "personas": "Personas",
    "sharedPersonas": "Shared Personas",
    "inviteCodes": "Invite Codes",
    "notifications": "Notifications",
    "settings": "Settings",
    "totalUsers": "Total Users",
    "premiumUsers": "Premium Users",
    "totalConversations": "Total Conversations",
    "totalMessages": "Total Messages",
    "banUser": "Ban User",
    "unbanUser": "Unban User",
    "upgradeUser": "Upgrade to Premium",
    "downgradeUser": "Downgrade to Free",
    "makeAdmin": "Make Admin",
    "removeAdmin": "Remove Admin",
    "createInviteCode": "Create Invite Code",
    "approvePersona": "Approve Persona",
    "rejectPersona": "Reject Persona"
  },
  "errors": {
    "generic": "An unexpected error occurred",
    "network": "Network connection error",
    "unauthorized": "You are not authorized",
    "notFound": "Page not found",
    "rateLimited": "Rate limit exceeded",
    "serverError": "Server error",
    "invalidInput": "Invalid input data",
    "limitReached": "Maximum limit reached",
    "apiKeyInvalid": "Invalid API key",
    "modelNotFound": "Model not found"
  },
  "onboarding": {
    "welcome": "Welcome!",
    "step1Title": "Sidebar",
    "step1Description": "Find your conversations, folders, and favorites here",
    "step2Title": "Top Bar",
    "step2Description": "Select platform, model, and persona from here",
    "step3Title": "Personas",
    "step3Description": "Use ready-made personas or create your own",
    "step4Title": "Shortcuts",
    "step4Description": "Type / for quick access to built-in personas",
    "step5Title": "Settings & API Keys",
    "step5Description": "Add your own API keys for direct model access",
    "step6Title": "Get Started!",
    "step6Description": "You're ready to start chatting with AI",
    "skip": "Skip",
    "finish": "Start Using"
  }
}
""")

    # ──────────────────────────────────────────────
    # Database types file
    # ──────────────────────────────────────────────
    create_file("types/database.ts", """// أنواع قاعدة البيانات: تعريف هيكل Supabase الكامل

import type { Profile } from './user';
import type { Conversation, Message } from './chat';
import type { Persona, PersonaRating, PremiumPersonaTrial } from './persona';
import type { ApiKey, GlobalModel } from './api-key';
import type { Folder } from './folder';
import type { Notification } from './notification';
import type { InviteCode, InviteCodeUse } from './invite-code';

/**
 * تعريف هيكل قاعدة البيانات لـ Supabase
 */
export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: Profile;
        Insert: Omit<Profile, 'created_at' | 'updated_at'>;
        Update: Partial<Omit<Profile, 'id' | 'created_at'>>;
      };
      conversations: {
        Row: Conversation;
        Insert: Omit<Conversation, 'id' | 'created_at' | 'updated_at' | 'message_count' | 'total_tokens'>;
        Update: Partial<Omit<Conversation, 'id' | 'user_id' | 'created_at'>>;
      };
      messages: {
        Row: Message;
        Insert: Omit<Message, 'id' | 'created_at'>;
        Update: Partial<Omit<Message, 'id' | 'conversation_id' | 'created_at'>>;
      };
      personas: {
        Row: Persona;
        Insert: Omit<Persona, 'id' | 'created_at' | 'updated_at' | 'average_rating' | 'rating_count' | 'usage_count'>;
        Update: Partial<Omit<Persona, 'id' | 'created_at'>>;
      };
      persona_ratings: {
        Row: PersonaRating;
        Insert: Omit<PersonaRating, 'id' | 'created_at'>;
        Update: Partial<Omit<PersonaRating, 'id' | 'created_at'>>;
      };
      api_keys: {
        Row: ApiKey;
        Insert: Omit<ApiKey, 'id' | 'created_at'>;
        Update: Partial<Omit<ApiKey, 'id' | 'created_at'>>;
      };
      global_models: {
        Row: GlobalModel;
        Insert: Omit<GlobalModel, 'id' | 'created_at'>;
        Update: Partial<Omit<GlobalModel, 'id' | 'created_at'>>;
      };
      folders: {
        Row: Folder;
        Insert: Omit<Folder, 'id' | 'created_at'>;
        Update: Partial<Omit<Folder, 'id' | 'user_id' | 'created_at'>>;
      };
      invite_codes: {
        Row: InviteCode;
        Insert: Omit<InviteCode, 'id' | 'created_at' | 'current_uses'>;
        Update: Partial<Omit<InviteCode, 'id' | 'created_at' | 'created_by'>>;
      };
      invite_code_uses: {
        Row: InviteCodeUse;
        Insert: Omit<InviteCodeUse, 'id' | 'used_at'>;
        Update: never;
      };
      notifications: {
        Row: Notification;
        Insert: Omit<Notification, 'id' | 'created_at'>;
        Update: Partial<Omit<Notification, 'id' | 'created_at'>>;
      };
      premium_persona_trials: {
        Row: PremiumPersonaTrial;
        Insert: Omit<PremiumPersonaTrial, 'id' | 'used_at'>;
        Update: never;
      };
      user_favorites: {
        Row: UserFavorite;
        Insert: Omit<UserFavorite, 'id' | 'created_at'>;
        Update: Partial<Omit<UserFavorite, 'id' | 'user_id' | 'created_at'>>;
      };
      usage_stats: {
        Row: UsageStat;
        Insert: Omit<UsageStat, 'id'>;
        Update: Partial<Omit<UsageStat, 'id' | 'user_id' | 'date'>>;
      };
    };
    Functions: {
      is_admin: {
        Args: Record<string, never>;
        Returns: boolean;
      };
      is_super_admin: {
        Args: Record<string, never>;
        Returns: boolean;
      };
      get_user_role: {
        Args: Record<string, never>;
        Returns: string;
      };
      check_premium_expiry: {
        Args: Record<string, never>;
        Returns: number;
      };
      check_trial_expiry: {
        Args: Record<string, never>;
        Returns: number;
      };
    };
  };
}

/**
 * المفضلة - تطابق جدول user_favorites
 */
export interface UserFavorite {
  id: string;
  user_id: string;
  item_type: 'persona' | 'model';
  item_id: string;
  sort_order: number;
  created_at: string;
}

/**
 * إحصائيات الاستخدام - تطابق جدول usage_stats
 */
export interface UsageStat {
  id: string;
  user_id: string;
  date: string;
  messages_sent: number;
  tokens_used: number;
  conversations_created: number;
  persona_id_most_used: string | null;
}
""")

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 1A SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print("  GROUP A - Configuration:")
    print("    1. package.json")
    print("    2. next.config.js")
    print("    3. tailwind.config.ts")
    print("    4. tsconfig.json")
    print("    5. wrangler.toml")
    print("    6. .env.example")
    print("    7. middleware.ts")
    print("    +  postcss.config.js")
    print()
    print("  GROUP B - Database:")
    print("    8. supabase/schema.sql")
    print("    9. supabase/rls-policies.sql")
    print("    10. supabase/functions.sql")
    print("    11. supabase/seed.sql")
    print()
    print("  GROUP C - Utilities:")
    print("    12. app/globals.css")
    print("    13. app/manifest.json")
    print("    14. utils/cn.ts")
    print("    15. utils/constants.ts")
    print("    16. utils/formatters.ts")
    print("    17. utils/validators.ts")
    print("    18. utils/helpers.ts")
    print()
    print("  GROUP D - TypeScript Types:")
    print("    19. types/user.ts")
    print("    20. types/chat.ts")
    print("    21. types/persona.ts")
    print("    22. types/platform.ts")
    print("    23. types/api-key.ts")
    print("    24. types/folder.ts")
    print("    25. types/notification.ts")
    print("    26. types/invite-code.ts")
    print("    27. types/database.ts")
    print()
    print("  EXTRAS:")
    print("    28. i18n/config.ts")
    print("    29. i18n/ar.json")
    print("    30. i18n/en.json")
    print("    31. public/robots.txt")
    print()
    print("📝 NOTES:")
    print("  - All .ts/.tsx files start with Arabic comments")
    print("  - TypeScript strict mode enabled, NO 'any' types used")
    print("  - All database tables have RLS enabled")
    print("  - 14 tables, 7 functions with triggers defined")
    print("  - 4 system personas with full Arabic prompts seeded")
    print("  - Complete i18n files for Arabic and English")
    print("  - Middleware handles auth, admin, locale routing")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 1B: Supabase clients, AI providers, encryption, stores, hooks")
    print("  Phase 2: Authentication (login, register, route guard)")
    print("  Phase 3A/B/C: Chat system (streaming, messages, UI)")
    print("  Phase 4: API Keys management")
    print("  Phase 5A/B: Features (personas, folders, favorites, export)")
    print("  Phase 6A/B: Admin panel")
    print("  Phase 7: Final (onboarding, worker proxy, polish)")
    print()
    print("✅ Phase 1A Complete! Ready for Phase 1B.")


if __name__ == "__main__":
    main()
