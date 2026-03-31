#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_1b.py
=================
Phase 1B: Supabase Clients + Stores + I18N + Root Layout
Creates all foundational client, state management, and internationalization files.
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
    print("🚀 BUILD PHASE 1B: Supabase Clients + Stores + I18N + Layout")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # GROUP E: Supabase Clients (3 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group E: Supabase Client Files")
    print("-" * 40)

    # 1. lib/supabase-client.ts
    create_file("lib/supabase-client.ts", """// عميل Supabase للمتصفح: يُستخدم في المكونات على جانب العميل فقط
// نمط Singleton لضمان إنشاء عميل واحد فقط طوال دورة حياة التطبيق
import { createBrowserClient } from '@supabase/ssr';
import type { Database } from '@/types/database';

let browserClient: ReturnType<typeof createBrowserClient<Database>> | null = null;

/**
 * إنشاء أو إرجاع عميل Supabase للمتصفح
 * يستخدم نمط Singleton لتجنب إنشاء عملاء متعددين
 * @returns عميل Supabase للمتصفح
 */
export function createSupabaseBrowserClient() {
  if (browserClient) {
    return browserClient;
  }

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error(
      'Missing Supabase environment variables: NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY must be set'
    );
  }

  browserClient = createBrowserClient<Database>(supabaseUrl, supabaseAnonKey);

  return browserClient;
}

/**
 * الحصول على عميل Supabase للمتصفح (اختصار)
 */
export function getSupabaseBrowserClient() {
  return createSupabaseBrowserClient();
}
""")

    # 2. lib/supabase-server.ts
    create_file("lib/supabase-server.ts", """// عميل Supabase للخادم: يُستخدم في مسارات API و Server Components
// يتعامل مع الكوكيز تلقائياً للحفاظ على جلسة المستخدم
import { createServerClient, type CookieOptions } from '@supabase/ssr';
import { cookies } from 'next/headers';
import type { Database } from '@/types/database';

/**
 * إنشاء عميل Supabase للخادم مع إدارة الكوكيز
 * يُستخدم في Server Components ومسارات API
 * @returns عميل Supabase للخادم
 */
export function createSupabaseServerClient() {
  const cookieStore = cookies();

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error(
      'Missing Supabase environment variables: NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY must be set'
    );
  }

  return createServerClient<Database>(supabaseUrl, supabaseAnonKey, {
    cookies: {
      get(name: string) {
        return cookieStore.get(name)?.value;
      },
      set(name: string, value: string, options: CookieOptions) {
        try {
          cookieStore.set({ name, value, ...options });
        } catch {
          // يحدث عند استدعاء set في Server Component
          // يمكن تجاهله بأمان لأن الكوكيز ستُحدَّث في middleware
        }
      },
      remove(name: string, options: CookieOptions) {
        try {
          cookieStore.set({ name, value: '', ...options });
        } catch {
          // نفس السبب أعلاه
        }
      },
    },
  });
}

/**
 * إنشاء عميل Supabase للخادم مع إدارة الكوكيز من كائن Request
 * يُستخدم في مسارات API (Route Handlers)
 * @param request - كائن الطلب
 * @returns عميل Supabase للخادم مع كائن الاستجابة
 */
export function createSupabaseServerClientFromRequest(request: Request) {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error(
      'Missing Supabase environment variables'
    );
  }

  const cookieStore = cookies();

  return createServerClient<Database>(supabaseUrl, supabaseAnonKey, {
    cookies: {
      get(name: string) {
        return cookieStore.get(name)?.value;
      },
      set(name: string, value: string, options: CookieOptions) {
        try {
          cookieStore.set({ name, value, ...options });
        } catch {
          // تجاهل في حالة عدم إمكانية الكتابة
        }
      },
      remove(name: string, options: CookieOptions) {
        try {
          cookieStore.set({ name, value: '', ...options });
        } catch {
          // تجاهل في حالة عدم إمكانية الكتابة
        }
      },
    },
  });
}
""")

    # 3. lib/supabase-admin.ts
    create_file("lib/supabase-admin.ts", """// عميل Supabase الإداري: يتجاوز سياسات RLS بالكامل
// يُستخدم فقط في مسارات API على الخادم - لا يُعرَض للعميل أبداً
import { createClient } from '@supabase/supabase-js';
import type { Database } from '@/types/database';

let adminClient: ReturnType<typeof createClient<Database>> | null = null;

/**
 * إنشاء أو إرجاع عميل Supabase الإداري
 * يستخدم Service Role Key لتجاوز RLS
 * تحذير: لا تستخدم هذا العميل في كود العميل أبداً!
 * @returns عميل Supabase الإداري
 */
export function createSupabaseAdminClient() {
  if (adminClient) {
    return adminClient;
  }

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!supabaseUrl || !serviceRoleKey) {
    throw new Error(
      'Missing Supabase admin environment variables: NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set'
    );
  }

  adminClient = createClient<Database>(supabaseUrl, serviceRoleKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });

  return adminClient;
}

/**
 * الحصول على عميل Supabase الإداري (اختصار)
 */
export function getSupabaseAdminClient() {
  return createSupabaseAdminClient();
}
""")

    # ──────────────────────────────────────────────
    # GROUP F: Zustand Stores (6 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group F: Zustand Store Files")
    print("-" * 40)

    # 4. stores/authStore.ts
    create_file("stores/authStore.ts", """// مخزن المصادقة: يحفظ بيانات المستخدم والجلسة والدور
// لا يستخدم persist لأن بيانات المصادقة تأتي من Supabase عند كل تحميل
import { create } from 'zustand';
import type { Profile, Role } from '@/types/user';
import type { Session } from '@supabase/supabase-js';

/**
 * واجهة مخزن المصادقة
 */
interface AuthStore {
  /** الملف الشخصي للمستخدم الحالي */
  user: Profile | null;
  /** دور المستخدم الحالي */
  role: Role;
  /** جلسة Supabase */
  session: Session | null;
  /** هل المستخدم مدير خارق؟ */
  isSuperAdmin: boolean;
  /** هل استخدم المستخدم التجربة المجانية؟ */
  trialUsed: boolean;
  /** هل يتم تحميل بيانات المصادقة؟ */
  isLoading: boolean;
  /** هل المستخدم محظور؟ */
  isBanned: boolean;

  /** تعيين بيانات المستخدم */
  setUser: (user: Profile | null) => void;
  /** تعيين الدور */
  setRole: (role: Role) => void;
  /** تعيين الجلسة */
  setSession: (session: Session | null) => void;
  /** تعيين حالة المدير الخارق */
  setSuperAdmin: (isSuperAdmin: boolean) => void;
  /** تعيين حالة التجربة */
  setTrialUsed: (trialUsed: boolean) => void;
  /** تعيين حالة التحميل */
  setLoading: (isLoading: boolean) => void;
  /** تعيين حالة الحظر */
  setBanned: (isBanned: boolean) => void;
  /** مسح جميع بيانات المصادقة */
  clearAuth: () => void;
}

/**
 * مخزن المصادقة باستخدام Zustand
 */
export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  role: 'free',
  session: null,
  isSuperAdmin: false,
  trialUsed: false,
  isLoading: true,
  isBanned: false,

  setUser: (user) =>
    set({
      user,
      role: user?.role ?? 'free',
      isSuperAdmin: user?.is_super_admin ?? false,
      trialUsed: user?.trial_used ?? false,
      isBanned: user?.is_banned ?? false,
    }),

  setRole: (role) => set({ role }),

  setSession: (session) => set({ session }),

  setSuperAdmin: (isSuperAdmin) => set({ isSuperAdmin }),

  setTrialUsed: (trialUsed) => set({ trialUsed }),

  setLoading: (isLoading) => set({ isLoading }),

  setBanned: (isBanned) => set({ isBanned }),

  clearAuth: () =>
    set({
      user: null,
      role: 'free',
      session: null,
      isSuperAdmin: false,
      trialUsed: false,
      isLoading: false,
      isBanned: false,
    }),
}));
""")

    # 5. stores/chatStore.ts
    create_file("stores/chatStore.ts", """// مخزن الدردشة: يحفظ المحادثة الحالية والرسائل وحالة البث
// لا يستخدم persist لأن البيانات تأتي من قاعدة البيانات
import { create } from 'zustand';
import type { Conversation, Message } from '@/types/chat';

/**
 * واجهة مخزن الدردشة
 */
interface ChatStore {
  /** المحادثة الحالية */
  conversation: Conversation | null;
  /** قائمة الرسائل في المحادثة الحالية */
  messages: Message[];
  /** هل يتم إرسال رسالة؟ */
  isSending: boolean;
  /** هل يتم استقبال بث مباشر؟ */
  isStreaming: boolean;
  /** عدد الرسائل في المحادثة الحالية */
  messageCount: number;
  /** إجمالي الرموز المستخدمة */
  totalTokens: number;
  /** النص المتدفق حالياً (أثناء البث) */
  streamingContent: string;

  /** تعيين المحادثة الحالية */
  setConversation: (conversation: Conversation | null) => void;
  /** إضافة رسالة جديدة */
  addMessage: (message: Message) => void;
  /** تحديث آخر رسالة (للبث المباشر) */
  updateLastMessage: (content: string) => void;
  /** تعيين قائمة الرسائل */
  setMessages: (messages: Message[]) => void;
  /** تعيين حالة الإرسال */
  setSending: (isSending: boolean) => void;
  /** تعيين حالة البث */
  setStreaming: (isStreaming: boolean) => void;
  /** تعيين النص المتدفق */
  setStreamingContent: (content: string) => void;
  /** إضافة محتوى للنص المتدفق */
  appendStreamingContent: (chunk: string) => void;
  /** زيادة عدد الرسائل */
  incrementMessageCount: () => void;
  /** إضافة رموز مستخدمة */
  addTokens: (tokens: number) => void;
  /** مسح جميع بيانات الدردشة */
  clearChat: () => void;
}

/**
 * مخزن الدردشة باستخدام Zustand
 */
export const useChatStore = create<ChatStore>((set) => ({
  conversation: null,
  messages: [],
  isSending: false,
  isStreaming: false,
  messageCount: 0,
  totalTokens: 0,
  streamingContent: '',

  setConversation: (conversation) =>
    set({
      conversation,
      messageCount: conversation?.message_count ?? 0,
      totalTokens: conversation?.total_tokens ?? 0,
    }),

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  updateLastMessage: (content) =>
    set((state) => {
      const messages = [...state.messages];
      const lastIndex = messages.length - 1;
      if (lastIndex >= 0) {
        const lastMessage = messages[lastIndex];
        if (lastMessage) {
          messages[lastIndex] = { ...lastMessage, content };
        }
      }
      return { messages };
    }),

  setMessages: (messages) => set({ messages }),

  setSending: (isSending) => set({ isSending }),

  setStreaming: (isStreaming) => set({ isStreaming }),

  setStreamingContent: (content) => set({ streamingContent: content }),

  appendStreamingContent: (chunk) =>
    set((state) => ({
      streamingContent: state.streamingContent + chunk,
    })),

  incrementMessageCount: () =>
    set((state) => ({
      messageCount: state.messageCount + 1,
    })),

  addTokens: (tokens) =>
    set((state) => ({
      totalTokens: state.totalTokens + tokens,
    })),

  clearChat: () =>
    set({
      conversation: null,
      messages: [],
      isSending: false,
      isStreaming: false,
      messageCount: 0,
      totalTokens: 0,
      streamingContent: '',
    }),
}));
""")

    # 6. stores/uiStore.ts
    create_file("stores/uiStore.ts", """// مخزن واجهة المستخدم: يحفظ إعدادات الواجهة مع persist في localStorage
// يتضمن الشريط الجانبي، المظهر، اللغة، جولة التعريف
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

/**
 * نوع المظهر
 */
type Theme = 'dark' | 'light' | 'auto';

/**
 * نوع اللغة
 */
type Locale = 'ar' | 'en';

/**
 * واجهة مخزن واجهة المستخدم
 */
interface UIStore {
  /** هل الشريط الجانبي مفتوح؟ */
  sidebarOpen: boolean;
  /** هل الشريط الجانبي مطوي (أيقونات فقط)؟ */
  sidebarCollapsed: boolean;
  /** المظهر الحالي */
  theme: Theme;
  /** اللغة الحالية */
  locale: Locale;
  /** هل جولة التعريف نشطة؟ */
  tourActive: boolean;
  /** خطوة جولة التعريف الحالية */
  tourStep: number;

  /** تبديل حالة الشريط الجانبي */
  toggleSidebar: () => void;
  /** تعيين حالة الشريط الجانبي */
  setSidebarOpen: (open: boolean) => void;
  /** تبديل حالة طي الشريط الجانبي */
  collapseSidebar: () => void;
  /** تعيين المظهر */
  setTheme: (theme: Theme) => void;
  /** تعيين اللغة */
  setLocale: (locale: Locale) => void;
  /** تعيين حالة جولة التعريف */
  setTourActive: (active: boolean) => void;
  /** تعيين خطوة جولة التعريف */
  setTourStep: (step: number) => void;
}

/**
 * مخزن واجهة المستخدم مع الحفظ المحلي
 */
export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      sidebarCollapsed: false,
      theme: 'dark',
      locale: 'ar',
      tourActive: false,
      tourStep: 0,

      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),

      setSidebarOpen: (open) => set({ sidebarOpen: open }),

      collapseSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      setTheme: (theme) => set({ theme }),

      setLocale: (locale) => set({ locale }),

      setTourActive: (active) => set({ tourActive: active }),

      setTourStep: (step) => set({ tourStep: step }),
    }),
    {
      name: 'ui-store',
      storage: createJSONStorage(() => {
        if (typeof window !== 'undefined') {
          return localStorage;
        }
        return {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        };
      }),
      partialize: (state) => ({
        sidebarOpen: state.sidebarOpen,
        sidebarCollapsed: state.sidebarCollapsed,
        theme: state.theme,
        locale: state.locale,
      }),
    }
  )
);
""")

    # 7. stores/personaStore.ts
    create_file("stores/personaStore.ts", """// مخزن الشخصيات: يحفظ الشخصية النشطة والمفضلات مع persist
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Persona } from '@/types/persona';

/**
 * واجهة مخزن الشخصيات
 */
interface PersonaStore {
  /** الشخصية النشطة حالياً */
  activePersona: Persona | null;
  /** قائمة معرفات الشخصيات المفضلة */
  favoritePersonaIds: string[];

  /** تعيين الشخصية النشطة */
  setActivePersona: (persona: Persona | null) => void;
  /** مسح الشخصية النشطة */
  clearPersona: () => void;
  /** إضافة شخصية للمفضلة */
  addFavoritePersona: (id: string) => void;
  /** إزالة شخصية من المفضلة */
  removeFavoritePersona: (id: string) => void;
  /** التحقق من وجود شخصية في المفضلة */
  isFavoritePersona: (id: string) => boolean;
}

/**
 * مخزن الشخصيات مع الحفظ المحلي
 */
export const usePersonaStore = create<PersonaStore>()(
  persist(
    (set, get) => ({
      activePersona: null,
      favoritePersonaIds: [],

      setActivePersona: (persona) => set({ activePersona: persona }),

      clearPersona: () => set({ activePersona: null }),

      addFavoritePersona: (id) =>
        set((state) => {
          if (state.favoritePersonaIds.includes(id)) {
            return state;
          }
          return {
            favoritePersonaIds: [...state.favoritePersonaIds, id],
          };
        }),

      removeFavoritePersona: (id) =>
        set((state) => ({
          favoritePersonaIds: state.favoritePersonaIds.filter(
            (favId) => favId !== id
          ),
        })),

      isFavoritePersona: (id) => {
        return get().favoritePersonaIds.includes(id);
      },
    }),
    {
      name: 'persona-store',
      storage: createJSONStorage(() => {
        if (typeof window !== 'undefined') {
          return localStorage;
        }
        return {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        };
      }),
      partialize: (state) => ({
        favoritePersonaIds: state.favoritePersonaIds,
      }),
    }
  )
);
""")

    # 8. stores/platformStore.ts
    create_file("stores/platformStore.ts", """// مخزن المنصة: يحفظ المنصة والنموذج النشطين ونوع المفتاح مع persist
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { PlatformName, Model } from '@/types/platform';

/**
 * نوع المفتاح (عام أو خاص)
 */
type ApiType = 'global' | 'private';

/**
 * واجهة مخزن المنصة
 */
interface PlatformStore {
  /** المنصة النشطة حالياً */
  activePlatform: PlatformName;
  /** النموذج النشط حالياً */
  activeModel: string;
  /** نوع المفتاح المستخدم */
  apiType: ApiType;
  /** النماذج المتاحة للمنصة الحالية */
  availableModels: Model[];

  /** تعيين المنصة النشطة */
  setPlatform: (platform: PlatformName) => void;
  /** تعيين النموذج النشط */
  setModel: (model: string) => void;
  /** تعيين نوع المفتاح */
  setApiType: (apiType: ApiType) => void;
  /** تعيين النماذج المتاحة */
  setAvailableModels: (models: Model[]) => void;
}

/**
 * مخزن المنصة مع الحفظ المحلي
 */
export const usePlatformStore = create<PlatformStore>()(
  persist(
    (set) => ({
      activePlatform: 'openrouter',
      activeModel: '',
      apiType: 'global',
      availableModels: [],

      setPlatform: (platform) =>
        set({
          activePlatform: platform,
          activeModel: '',
          availableModels: [],
        }),

      setModel: (model) => set({ activeModel: model }),

      setApiType: (apiType) => set({ apiType }),

      setAvailableModels: (models) => set({ availableModels: models }),
    }),
    {
      name: 'platform-store',
      storage: createJSONStorage(() => {
        if (typeof window !== 'undefined') {
          return localStorage;
        }
        return {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        };
      }),
      partialize: (state) => ({
        activePlatform: state.activePlatform,
        activeModel: state.activeModel,
        apiType: state.apiType,
      }),
    }
  )
);
""")

    # 9. stores/settingsStore.ts
    create_file("stores/settingsStore.ts", """// مخزن الإعدادات: يحفظ آخر منصة ونموذج مستخدمين مع persist
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { PlatformName } from '@/types/platform';

/**
 * واجهة مخزن الإعدادات
 */
interface SettingsStore {
  /** آخر منصة مستخدمة */
  lastUsedPlatform: PlatformName | null;
  /** آخر نموذج مستخدم */
  lastUsedModel: string | null;

  /** تعيين آخر منصة ونموذج مستخدمين */
  setLastUsed: (platform: PlatformName, model: string) => void;
}

/**
 * مخزن الإعدادات مع الحفظ المحلي
 */
export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      lastUsedPlatform: null,
      lastUsedModel: null,

      setLastUsed: (platform, model) =>
        set({
          lastUsedPlatform: platform,
          lastUsedModel: model,
        }),
    }),
    {
      name: 'settings-store',
      storage: createJSONStorage(() => {
        if (typeof window !== 'undefined') {
          return localStorage;
        }
        return {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        };
      }),
    }
  )
);
""")

    # ──────────────────────────────────────────────
    # GROUP G: Internationalization (3 files)
    # ──────────────────────────────────────────────
    print("\n📁 Group G: Internationalization Files")
    print("-" * 40)

    # 10. i18n/config.ts
    create_file("i18n/config.ts", """// إعدادات التدويل (i18n): تحديد اللغات المدعومة واللغة الافتراضية
// يُستخدم مع next-intl لتحميل ملفات الترجمة تلقائياً
import { getRequestConfig } from 'next-intl/server';

/**
 * اللغات المدعومة
 */
export const locales = ['ar', 'en'] as const;

/**
 * نوع اللغة
 */
export type Locale = (typeof locales)[number];

/**
 * اللغة الافتراضية
 */
export const defaultLocale: Locale = 'ar';

/**
 * بادئة اللغة في المسار
 */
export const localePrefix = 'always' as const;

/**
 * تحميل إعدادات اللغة حسب الطلب
 */
export default getRequestConfig(async ({ locale }) => {
  const validLocale: Locale = locales.includes(locale as Locale)
    ? (locale as Locale)
    : defaultLocale;

  return {
    messages: (await import(`@/i18n/${validLocale}.json`)).default,
  };
});
""")

    # 11. i18n/ar.json - COMPLETE Arabic translations
    create_file("i18n/ar.json", """{
  "auth": {
    "login_title": "مرحباً بعودتك",
    "register_title": "إنشاء حساب جديد",
    "email_label": "البريد الإلكتروني",
    "email_placeholder": "أدخل بريدك الإلكتروني",
    "password_label": "كلمة المرور",
    "password_placeholder": "أدخل كلمة المرور",
    "confirm_password_label": "تأكيد كلمة المرور",
    "confirm_password_placeholder": "أعد إدخال كلمة المرور",
    "display_name_label": "الاسم المعروض",
    "display_name_placeholder": "أدخل اسمك المعروض",
    "login_button": "تسجيل الدخول",
    "register_button": "إنشاء الحساب",
    "logging_in": "جاري تسجيل الدخول...",
    "registering": "جاري إنشاء الحساب...",
    "logout": "تسجيل الخروج",
    "logout_confirm": "هل أنت متأكد من تسجيل الخروج؟",
    "no_account": "ليس لديك حساب؟",
    "have_account": "لديك حساب بالفعل؟",
    "password_strength_weak": "ضعيفة",
    "password_strength_medium": "متوسطة",
    "password_strength_strong": "قوية",
    "passwords_not_match": "كلمات المرور غير متطابقة",
    "error_invalid_credentials": "البريد الإلكتروني أو كلمة المرور غير صحيحة",
    "error_email_exists": "هذا البريد الإلكتروني مسجل بالفعل",
    "error_weak_password": "كلمة المرور ضعيفة جداً، يجب أن تكون 8 أحرف على الأقل",
    "error_banned": "تم حظر حسابك. تواصل مع الإدارة.",
    "error_network": "خطأ في الاتصال بالشبكة. حاول مرة أخرى.",
    "error_generic": "حدث خطأ غير متوقع. حاول مرة أخرى."
  },
  "chat": {
    "new_conversation": "محادثة جديدة",
    "send": "إرسال",
    "stop": "إيقاف",
    "typing": "يكتب...",
    "empty_welcome": "مرحباً بك في منصة الدردشة بالذكاء الاصطناعي",
    "empty_subtitle": "اختر نموذجاً وابدأ محادثة جديدة، أو استخدم شخصية متخصصة",
    "suggestion_1": "اكتب لي منشور لينكدإن احترافي",
    "suggestion_2": "ساعدني في العصف الذهني لمشروع جديد",
    "suggestion_3": "حسّن لي هذا الأمر (Prompt)",
    "suggestion_4": "اكتب لي إيميل رسمي",
    "message_limit_title": "وصلت للحد الأقصى",
    "message_limit_body": "وصلت لحد {limit} رسالة في هذه المحادثة. يمكنك بدء محادثة جديدة.",
    "keep_conversation": "الاحتفاظ بالمحادثة",
    "delete_conversation": "حذف المحادثة",
    "export_conversation": "تصدير المحادثة",
    "start_new": "بدء محادثة جديدة",
    "rate_limit_wait": "يرجى الانتظار",
    "rate_limit_seconds": "{seconds} ثانية",
    "rate_limit_tip": "ترقِّ للحساب المميز للتخلص من وقت الانتظار",
    "no_persona": "بدون شخصية",
    "switched_to_persona": "تم التبديل إلى: {name}",
    "conversation_deleted": "تم حذف المحادثة",
    "conversation_exported": "تم تصدير المحادثة بنجاح",
    "copy_message": "نسخ الرسالة",
    "message_copied": "تم نسخ الرسالة",
    "regenerate": "إعادة التوليد",
    "tokens_used": "الرموز المستخدمة",
    "response_time": "وقت الاستجابة",
    "model_used": "النموذج المستخدم",
    "no_messages": "لا توجد رسائل بعد",
    "type_message": "اكتب رسالتك هنا...",
    "type_slash": "اكتب / لاستخدام شخصية سريعة",
    "messages_remaining": "{count} رسالة متبقية",
    "messages_used": "{used} من {total} رسالة"
  },
  "sidebar": {
    "search_placeholder": "بحث في المحادثات...",
    "new_chat": "محادثة جديدة",
    "folders": "المجلدات",
    "add_folder": "إضافة مجلد",
    "rename_folder": "إعادة تسمية المجلد",
    "delete_folder": "حذف المجلد",
    "delete_folder_confirm": "هل أنت متأكد من حذف هذا المجلد؟ سيتم نقل المحادثات للقائمة الرئيسية.",
    "move_conversations": "نقل المحادثات",
    "favorites": "المفضلة",
    "no_favorites": "لا توجد عناصر في المفضلة",
    "personas": "الشخصيات",
    "view_all": "عرض الكل",
    "settings": "الإعدادات",
    "theme_dark": "مظلم",
    "theme_light": "فاتح",
    "theme_auto": "تلقائي",
    "language_ar": "العربية",
    "language_en": "English",
    "logout": "تسجيل الخروج",
    "rename": "إعادة التسمية",
    "move_to_folder": "نقل إلى مجلد",
    "export": "تصدير",
    "delete": "حذف",
    "delete_confirm": "هل أنت متأكد من حذف هذه المحادثة؟",
    "today": "اليوم",
    "yesterday": "أمس",
    "this_week": "هذا الأسبوع",
    "older": "أقدم",
    "no_conversations": "لا توجد محادثات",
    "start_new_chat": "ابدأ محادثة جديدة",
    "folder_name_placeholder": "اسم المجلد",
    "conversations_count": "{count} محادثة",
    "add_to_favorites": "إضافة للمفضلة",
    "remove_from_favorites": "إزالة من المفضلة"
  },
  "header": {
    "select_platform": "اختر المنصة",
    "select_model": "اختر النموذج",
    "no_model": "لا يوجد نموذج متاح",
    "add_api_key_hint": "أضف مفتاح API للوصول لنماذج إضافية",
    "switch_persona": "تبديل الشخصية",
    "no_persona": "بدون شخصية",
    "settings_profile": "الملف الشخصي",
    "settings_api_keys": "مفاتيح API",
    "settings_export": "تصدير البيانات",
    "settings_tour": "جولة تعريفية",
    "settings_tokens": "عداد الرموز",
    "settings_admin": "لوحة الإدارة",
    "settings_logout": "تسجيل الخروج",
    "global_api": "مفتاح عام",
    "private_api": "مفتاح خاص",
    "switch_to_global": "التبديل للمفتاح العام",
    "switch_to_private": "التبديل للمفتاح الخاص",
    "menu": "القائمة",
    "account_free": "حساب مجاني",
    "account_premium": "حساب مميز",
    "account_admin": "حساب مدير"
  },
  "personas": {
    "library_title": "مكتبة الشخصيات",
    "tab_basic": "الأساسية",
    "tab_premium": "المميزة",
    "tab_custom": "المخصصة",
    "tab_community": "المجتمع",
    "create_title": "إنشاء شخصية جديدة",
    "edit_title": "تعديل الشخصية",
    "name_label": "اسم الشخصية",
    "name_placeholder": "مثال: خبير التسويق الرقمي",
    "description_label": "وصف الشخصية",
    "description_placeholder": "وصف مختصر لتخصص الشخصية ومهاراتها",
    "category_label": "الفئة",
    "select_category": "اختر فئة",
    "icon_label": "أيقونة الشخصية",
    "system_prompt_label": "نص النظام (System Prompt)",
    "system_prompt_placeholder": "اكتب التعليمات التفصيلية التي تحدد سلوك وتخصص هذه الشخصية...",
    "save": "حفظ الشخصية",
    "save_and_share": "حفظ ومشاركة",
    "preview": "معاينة",
    "cancel": "إلغاء",
    "share_with_community": "مشاركة مع المجتمع",
    "share_submitted": "تم إرسال الشخصية للمراجعة",
    "share_pending": "في انتظار موافقة الإدارة",
    "upgrade_prompt": "هذه الشخصية متاحة للمشتركين المميزين فقط",
    "trial_message_button": "تجربة رسالة واحدة مجاناً",
    "trial_used": "تم استخدام الرسالة التجريبية",
    "copy_persona": "نسخ الشخصية",
    "copied": "تم نسخ نص النظام",
    "use_persona": "استخدام الشخصية",
    "rate_persona": "تقييم الشخصية",
    "persona_count": "{count} شخصية",
    "at_limit_message": "وصلت للحد الأقصى ({limit}) من الشخصيات المخصصة",
    "categories": {
      "writing": "كتابة",
      "marketing": "تسويق",
      "programming": "برمجة",
      "education": "تعليم",
      "translation": "ترجمة",
      "general": "عام"
    },
    "no_personas": "لا توجد شخصيات",
    "search_personas": "بحث في الشخصيات...",
    "active": "نشطة",
    "inactive": "غير نشطة",
    "rating_stars": "{rating} من 5",
    "used_times": "استُخدمت {count} مرة",
    "slash_hint": "استخدم /{command} في مربع الكتابة"
  },
  "settings": {
    "title": "الإعدادات",
    "profile_tab": "الملف الشخصي",
    "api_keys_tab": "مفاتيح API",
    "language_tab": "اللغة",
    "theme_tab": "المظهر",
    "export_tab": "تصدير واستيراد",
    "display_name": "الاسم المعروض",
    "display_name_placeholder": "أدخل اسمك المعروض",
    "email": "البريد الإلكتروني",
    "account_type": "نوع الحساب",
    "join_date": "تاريخ الانضمام",
    "total_conversations": "إجمالي المحادثات",
    "total_messages": "إجمالي الرسائل",
    "total_tokens": "إجمالي الرموز",
    "trial_button": "بدء التجربة المجانية (3 أيام)",
    "trial_success": "تم تفعيل التجربة المجانية بنجاح!",
    "trial_already_used": "لقد استخدمت التجربة المجانية مسبقاً",
    "trial_active": "التجربة المجانية نشطة",
    "trial_expires": "تنتهي في: {date}",
    "invite_code_label": "كود الدعوة",
    "invite_code_placeholder": "أدخل كود الدعوة",
    "activate_code": "تفعيل الكود",
    "code_success": "تم تفعيل الكود بنجاح! تمت ترقيتك للحساب المميز.",
    "code_invalid": "كود الدعوة غير صالح",
    "code_expired": "كود الدعوة منتهي الصلاحية",
    "code_used": "كود الدعوة استُخدم بالكامل",
    "code_already_used": "لقد استخدمت هذا الكود مسبقاً",
    "add_key": "إضافة مفتاح API",
    "platform_label": "المنصة",
    "key_label": "مفتاح API",
    "key_placeholder": "أدخل مفتاح API",
    "label_label": "تسمية المفتاح",
    "label_placeholder": "مثال: مفتاح OpenAI الرئيسي",
    "save_key": "حفظ المفتاح",
    "delete_key": "حذف المفتاح",
    "delete_key_confirm": "هل أنت متأكد من حذف هذا المفتاح؟",
    "key_count": "{count} مفتاح",
    "key_limit_message": "وصلت للحد الأقصى ({limit}) من مفاتيح API للحسابات المجانية",
    "key_added": "تم إضافة المفتاح بنجاح",
    "key_deleted": "تم حذف المفتاح",
    "key_invalid": "مفتاح API غير صالح لهذه المنصة",
    "export_settings": "تصدير الإعدادات والمحادثات",
    "export_description": "تصدير جميع محادثاتك وإعداداتك كملف JSON",
    "export_excludes": "لا يتضمن التصدير مفاتيح API لأسباب أمنية",
    "export_button": "تصدير البيانات",
    "export_as_pdf": "تصدير كـ PDF",
    "export_as_json": "تصدير كـ JSON",
    "export_as_markdown": "تصدير كـ Markdown",
    "import_settings": "استيراد الإعدادات",
    "import_replace": "استبدال البيانات الحالية",
    "import_merge": "دمج مع البيانات الحالية",
    "import_success": "تم استيراد البيانات بنجاح",
    "import_error": "خطأ في استيراد البيانات",
    "import_invalid_file": "الملف غير صالح",
    "import_button": "استيراد البيانات",
    "saved": "تم حفظ الإعدادات",
    "save_error": "خطأ في حفظ الإعدادات"
  },
  "admin": {
    "dashboard": "لوحة المعلومات",
    "users": "المستخدمون",
    "api_keys": "مفاتيح API",
    "models": "النماذج",
    "personas": "الشخصيات",
    "shared_personas": "الشخصيات المشتركة",
    "invite_codes": "أكواد الدعوة",
    "notifications": "الإشعارات",
    "system_settings": "إعدادات النظام",
    "total_users": "إجمالي المستخدمين",
    "active_today": "نشط اليوم",
    "premium_accounts": "حسابات مميزة",
    "total_conversations_stat": "إجمالي المحادثات",
    "messages_today": "رسائل اليوم",
    "tokens_today": "رموز اليوم",
    "top_personas": "أكثر الشخصيات استخداماً",
    "recent_notifications": "آخر الإشعارات",
    "recent_users": "آخر المستخدمين",
    "user_table_name": "الاسم",
    "user_table_email": "البريد الإلكتروني",
    "user_table_role": "الدور",
    "user_table_joined": "تاريخ الانضمام",
    "user_table_last_active": "آخر نشاط",
    "user_table_status": "الحالة",
    "user_table_conversations": "المحادثات",
    "user_table_messages": "الرسائل",
    "user_table_actions": "الإجراءات",
    "upgrade_premium": "ترقية للمميز",
    "downgrade_free": "تخفيض للمجاني",
    "upgrade_admin": "ترقية لمدير",
    "downgrade_admin": "إزالة صلاحية الإدارة",
    "ban_user": "حظر المستخدم",
    "unban_user": "إلغاء الحظر",
    "delete_user": "حذف المستخدم",
    "delete_user_confirm": "هل أنت متأكد من حذف هذا المستخدم وجميع بياناته؟",
    "delete_user_type": "اكتب DELETE للتأكيد",
    "set_duration": "تحديد المدة",
    "duration_days": "{days} يوم",
    "duration_permanent": "دائم",
    "add_api_key": "إضافة مفتاح API عام",
    "edit_key": "تعديل المفتاح",
    "delete_key_admin": "حذف المفتاح",
    "toggle_active": "تفعيل/تعطيل",
    "model_name": "اسم النموذج",
    "model_id": "معرف النموذج",
    "add_model": "إضافة نموذج",
    "auto_fetch": "جلب تلقائي",
    "fetch_models": "جلب النماذج",
    "fetching_models": "جاري جلب النماذج...",
    "models_fetched": "تم جلب {count} نموذج",
    "reorder": "إعادة الترتيب",
    "add_system_persona": "إضافة شخصية نظامية",
    "add_premium_persona": "إضافة شخصية مميزة",
    "edit_persona": "تعديل الشخصية",
    "delete_persona": "حذف الشخصية",
    "convert_to_system": "تحويل لنظامية",
    "cannot_delete_original": "لا يمكن حذف الشخصيات النظامية الأصلية",
    "pending_personas": "شخصيات في انتظار الموافقة",
    "approve": "موافقة",
    "reject": "رفض",
    "preview_persona": "معاينة الشخصية",
    "edit_before_approve": "تعديل قبل الموافقة",
    "no_pending": "لا توجد شخصيات في انتظار الموافقة",
    "create_invite": "إنشاء كود دعوة",
    "code_label": "الكود",
    "max_uses": "الحد الأقصى للاستخدام",
    "premium_duration": "مدة الاشتراك المميز",
    "code_expiry": "تاريخ الانتهاء",
    "generate_code": "توليد كود",
    "copy_link": "نسخ الرابط",
    "link_copied": "تم نسخ الرابط",
    "deactivate_code": "تعطيل الكود",
    "delete_code": "حذف الكود",
    "view_uses": "عرض الاستخدامات",
    "mark_all_read": "تعليم الكل كمقروء",
    "filter_by_type": "تصفية حسب النوع",
    "filter_by_priority": "تصفية حسب الأولوية",
    "filter_by_status": "تصفية حسب الحالة",
    "delete_notification": "حذف الإشعار",
    "delete_old": "حذف الإشعارات القديمة",
    "telegram_token": "رمز بوت تلغرام",
    "telegram_chat_id": "معرف محادثة تلغرام",
    "test_connection": "اختبار الاتصال",
    "test_success": "تم إرسال رسالة الاختبار بنجاح",
    "test_failed": "فشل اختبار الاتصال",
    "notification_toggles": "تفعيل/تعطيل أنواع الإشعارات",
    "save_settings": "حفظ الإعدادات",
    "system_limits": "حدود النظام",
    "limit_free_messages": "رسائل مجانية قبل التأخير",
    "limit_free_delay": "تأخير الحساب المجاني (ثانية)",
    "limit_premium_delay": "تأخير الحساب المميز (ثانية)",
    "limit_message_per_chat": "حد الرسائل لكل محادثة",
    "limit_max_conversations": "حد المحادثات للمجاني",
    "limit_max_api_keys": "حد مفاتيح API للمجاني",
    "limit_max_personas": "حد الشخصيات للمجاني",
    "limit_trial_days": "مدة التجربة (أيام)",
    "user_updated": "تم تحديث المستخدم",
    "user_deleted": "تم حذف المستخدم",
    "key_created": "تم إنشاء المفتاح",
    "key_updated": "تم تحديث المفتاح",
    "key_deleted": "تم حذف المفتاح",
    "model_created": "تم إضافة النموذج",
    "model_deleted": "تم حذف النموذج",
    "persona_created": "تم إنشاء الشخصية",
    "persona_updated": "تم تحديث الشخصية",
    "persona_deleted": "تم حذف الشخصية",
    "persona_approved": "تمت الموافقة على الشخصية",
    "persona_rejected": "تم رفض الشخصية",
    "code_created": "تم إنشاء الكود",
    "code_deactivated": "تم تعطيل الكود",
    "code_deleted": "تم حذف الكود",
    "settings_saved": "تم حفظ الإعدادات",
    "no_data": "لا توجد بيانات",
    "refresh": "تحديث"
  },
  "notifications": {
    "user_registered": "مستخدم جديد مسجل",
    "trial_requested": "طلب تجربة مجانية",
    "trial_expired": "انتهاء فترة تجريبية",
    "premium_expired": "انتهاء اشتراك مميز",
    "persona_shared": "شخصية مشتركة جديدة",
    "api_low_balance": "رصيد API منخفض",
    "api_depleted": "نفاد رصيد API",
    "system_error": "خطأ في النظام",
    "invite_code_used": "استخدام كود دعوة"
  },
  "onboarding": {
    "step1_title": "الشريط الجانبي",
    "step1_message": "هنا تجد جميع محادثاتك منظمة حسب التاريخ والمجلدات. يمكنك إنشاء مجلدات جديدة وتنظيم محادثاتك بسهولة.",
    "step2_title": "الشريط العلوي",
    "step2_message": "اختر المنصة والنموذج من هنا. يمكنك التبديل بين 7 منصات ذكاء اصطناعي مختلفة.",
    "step3_title": "الشخصيات",
    "step3_message": "استخدم شخصيات جاهزة متخصصة في مجالات مختلفة، أو أنشئ شخصياتك الخاصة لتخصيص تجربة الدردشة.",
    "step4_title": "الاختصارات السريعة",
    "step4_message": "اكتب / في مربع الكتابة للوصول السريع للشخصيات المدمجة: /linkedin /brainstorm /prompt /email",
    "step5_title": "الإعدادات ومفاتيح API",
    "step5_message": "أضف مفاتيح API الخاصة بك من الإعدادات للوصول المباشر للنماذج. المفاتيح مشفرة بتقنية AES-256.",
    "step6_title": "ابدأ الآن!",
    "step6_message": "أنت جاهز لبدء المحادثة. اختر نموذجاً من الأعلى واكتب رسالتك الأولى!",
    "skip": "تخطي",
    "next": "التالي",
    "previous": "السابق",
    "start_using": "ابدأ الاستخدام"
  },
  "common": {
    "loading": "جاري التحميل...",
    "save": "حفظ",
    "cancel": "إلغاء",
    "delete": "حذف",
    "edit": "تعديل",
    "create": "إنشاء",
    "copy": "نسخ",
    "copied": "تم النسخ!",
    "confirm": "تأكيد",
    "yes": "نعم",
    "no": "لا",
    "ok": "موافق",
    "close": "إغلاق",
    "search": "بحث",
    "filter": "تصفية",
    "sort": "ترتيب",
    "export_label": "تصدير",
    "import_label": "استيراد",
    "refresh": "تحديث",
    "back": "رجوع",
    "next_label": "التالي",
    "previous_label": "السابق",
    "skip_label": "تخطي",
    "done": "تم",
    "required": "مطلوب",
    "optional": "اختياري",
    "unlimited": "غير محدود",
    "permanent": "دائم",
    "days": "أيام",
    "active": "نشط",
    "inactive": "غير نشط",
    "banned": "محظور",
    "all": "الكل",
    "no_results": "لا توجد نتائج",
    "error_occurred": "حدث خطأ",
    "try_again": "حاول مرة أخرى",
    "unauthorized": "غير مصرح لك",
    "not_found": "غير موجود",
    "free": "مجاني",
    "premium": "مميز",
    "admin": "مدير",
    "online": "متصل",
    "offline": "غير متصل"
  },
  "errors": {
    "generic": "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.",
    "network": "خطأ في الاتصال بالشبكة. تحقق من اتصالك بالإنترنت.",
    "unauthorized": "غير مصرح لك بالوصول إلى هذه الصفحة.",
    "not_found": "الصفحة المطلوبة غير موجودة.",
    "rate_limited": "تم تجاوز حد الطلبات. يرجى الانتظار قليلاً.",
    "limit_reached": "وصلت للحد الأقصى المسموح به لحسابك.",
    "invalid_input": "البيانات المدخلة غير صالحة. تحقق من المدخلات وحاول مرة أخرى.",
    "banned_account": "تم حظر حسابك. تواصل مع الإدارة للمزيد من المعلومات.",
    "server_error": "خطأ في الخادم. يرجى المحاولة لاحقاً.",
    "api_key_invalid": "مفتاح API غير صالح أو منتهي الصلاحية.",
    "model_not_available": "النموذج المحدد غير متاح حالياً.",
    "conversation_not_found": "المحادثة غير موجودة أو تم حذفها.",
    "persona_not_found": "الشخصية غير موجودة.",
    "file_too_large": "الملف كبير جداً.",
    "unsupported_format": "تنسيق الملف غير مدعوم."
  }
}
""")

    # 12. i18n/en.json - COMPLETE English translations
    create_file("i18n/en.json", """{
  "auth": {
    "login_title": "Welcome Back",
    "register_title": "Create New Account",
    "email_label": "Email",
    "email_placeholder": "Enter your email",
    "password_label": "Password",
    "password_placeholder": "Enter your password",
    "confirm_password_label": "Confirm Password",
    "confirm_password_placeholder": "Re-enter your password",
    "display_name_label": "Display Name",
    "display_name_placeholder": "Enter your display name",
    "login_button": "Login",
    "register_button": "Create Account",
    "logging_in": "Logging in...",
    "registering": "Creating account...",
    "logout": "Logout",
    "logout_confirm": "Are you sure you want to logout?",
    "no_account": "Don't have an account?",
    "have_account": "Already have an account?",
    "password_strength_weak": "Weak",
    "password_strength_medium": "Medium",
    "password_strength_strong": "Strong",
    "passwords_not_match": "Passwords do not match",
    "error_invalid_credentials": "Invalid email or password",
    "error_email_exists": "This email is already registered",
    "error_weak_password": "Password is too weak, must be at least 8 characters",
    "error_banned": "Your account has been banned. Contact administration.",
    "error_network": "Network connection error. Please try again.",
    "error_generic": "An unexpected error occurred. Please try again."
  },
  "chat": {
    "new_conversation": "New Conversation",
    "send": "Send",
    "stop": "Stop",
    "typing": "Typing...",
    "empty_welcome": "Welcome to AI Chat Platform",
    "empty_subtitle": "Select a model and start a new conversation, or use a specialized persona",
    "suggestion_1": "Write me a professional LinkedIn post",
    "suggestion_2": "Help me brainstorm for a new project",
    "suggestion_3": "Improve this prompt for me",
    "suggestion_4": "Write me a formal email",
    "message_limit_title": "Limit Reached",
    "message_limit_body": "You've reached the {limit} message limit for this conversation. You can start a new one.",
    "keep_conversation": "Keep Conversation",
    "delete_conversation": "Delete Conversation",
    "export_conversation": "Export Conversation",
    "start_new": "Start New Conversation",
    "rate_limit_wait": "Please wait",
    "rate_limit_seconds": "{seconds} seconds",
    "rate_limit_tip": "Upgrade to Premium to reduce wait time",
    "no_persona": "No Persona",
    "switched_to_persona": "Switched to: {name}",
    "conversation_deleted": "Conversation deleted",
    "conversation_exported": "Conversation exported successfully",
    "copy_message": "Copy Message",
    "message_copied": "Message copied",
    "regenerate": "Regenerate",
    "tokens_used": "Tokens used",
    "response_time": "Response time",
    "model_used": "Model used",
    "no_messages": "No messages yet",
    "type_message": "Type your message here...",
    "type_slash": "Type / to use a quick persona",
    "messages_remaining": "{count} messages remaining",
    "messages_used": "{used} of {total} messages"
  },
  "sidebar": {
    "search_placeholder": "Search conversations...",
    "new_chat": "New Chat",
    "folders": "Folders",
    "add_folder": "Add Folder",
    "rename_folder": "Rename Folder",
    "delete_folder": "Delete Folder",
    "delete_folder_confirm": "Are you sure you want to delete this folder? Conversations will be moved to the main list.",
    "move_conversations": "Move Conversations",
    "favorites": "Favorites",
    "no_favorites": "No favorites yet",
    "personas": "Personas",
    "view_all": "View All",
    "settings": "Settings",
    "theme_dark": "Dark",
    "theme_light": "Light",
    "theme_auto": "Auto",
    "language_ar": "العربية",
    "language_en": "English",
    "logout": "Logout",
    "rename": "Rename",
    "move_to_folder": "Move to Folder",
    "export": "Export",
    "delete": "Delete",
    "delete_confirm": "Are you sure you want to delete this conversation?",
    "today": "Today",
    "yesterday": "Yesterday",
    "this_week": "This Week",
    "older": "Older",
    "no_conversations": "No conversations",
    "start_new_chat": "Start a new conversation",
    "folder_name_placeholder": "Folder name",
    "conversations_count": "{count} conversations",
    "add_to_favorites": "Add to favorites",
    "remove_from_favorites": "Remove from favorites"
  },
  "header": {
    "select_platform": "Select Platform",
    "select_model": "Select Model",
    "no_model": "No model available",
    "add_api_key_hint": "Add an API key to access more models",
    "switch_persona": "Switch Persona",
    "no_persona": "No Persona",
    "settings_profile": "Profile",
    "settings_api_keys": "API Keys",
    "settings_export": "Export Data",
    "settings_tour": "Guided Tour",
    "settings_tokens": "Token Counter",
    "settings_admin": "Admin Panel",
    "settings_logout": "Logout",
    "global_api": "Global Key",
    "private_api": "Private Key",
    "switch_to_global": "Switch to Global Key",
    "switch_to_private": "Switch to Private Key",
    "menu": "Menu",
    "account_free": "Free Account",
    "account_premium": "Premium Account",
    "account_admin": "Admin Account"
  },
  "personas": {
    "library_title": "Persona Library",
    "tab_basic": "Basic",
    "tab_premium": "Premium",
    "tab_custom": "Custom",
    "tab_community": "Community",
    "create_title": "Create New Persona",
    "edit_title": "Edit Persona",
    "name_label": "Persona Name",
    "name_placeholder": "Example: Digital Marketing Expert",
    "description_label": "Persona Description",
    "description_placeholder": "Brief description of the persona's specialization and skills",
    "category_label": "Category",
    "select_category": "Select a category",
    "icon_label": "Persona Icon",
    "system_prompt_label": "System Prompt",
    "system_prompt_placeholder": "Write detailed instructions that define this persona's behavior and specialization...",
    "save": "Save Persona",
    "save_and_share": "Save & Share",
    "preview": "Preview",
    "cancel": "Cancel",
    "share_with_community": "Share with Community",
    "share_submitted": "Persona submitted for review",
    "share_pending": "Pending admin approval",
    "upgrade_prompt": "This persona is available for Premium subscribers only",
    "trial_message_button": "Try one message for free",
    "trial_used": "Trial message already used",
    "copy_persona": "Copy Persona",
    "copied": "System prompt copied",
    "use_persona": "Use Persona",
    "rate_persona": "Rate Persona",
    "persona_count": "{count} personas",
    "at_limit_message": "You've reached the maximum ({limit}) custom personas",
    "categories": {
      "writing": "Writing",
      "marketing": "Marketing",
      "programming": "Programming",
      "education": "Education",
      "translation": "Translation",
      "general": "General"
    },
    "no_personas": "No personas found",
    "search_personas": "Search personas...",
    "active": "Active",
    "inactive": "Inactive",
    "rating_stars": "{rating} out of 5",
    "used_times": "Used {count} times",
    "slash_hint": "Type /{command} in the message box"
  },
  "settings": {
    "title": "Settings",
    "profile_tab": "Profile",
    "api_keys_tab": "API Keys",
    "language_tab": "Language",
    "theme_tab": "Theme",
    "export_tab": "Export & Import",
    "display_name": "Display Name",
    "display_name_placeholder": "Enter your display name",
    "email": "Email",
    "account_type": "Account Type",
    "join_date": "Join Date",
    "total_conversations": "Total Conversations",
    "total_messages": "Total Messages",
    "total_tokens": "Total Tokens",
    "trial_button": "Start Free Trial (3 days)",
    "trial_success": "Free trial activated successfully!",
    "trial_already_used": "You've already used the free trial",
    "trial_active": "Free trial is active",
    "trial_expires": "Expires on: {date}",
    "invite_code_label": "Invite Code",
    "invite_code_placeholder": "Enter invite code",
    "activate_code": "Activate Code",
    "code_success": "Code activated! You've been upgraded to Premium.",
    "code_invalid": "Invalid invite code",
    "code_expired": "Invite code has expired",
    "code_used": "Invite code has been fully used",
    "code_already_used": "You've already used this code",
    "add_key": "Add API Key",
    "platform_label": "Platform",
    "key_label": "API Key",
    "key_placeholder": "Enter API key",
    "label_label": "Key Label",
    "label_placeholder": "Example: Main OpenAI Key",
    "save_key": "Save Key",
    "delete_key": "Delete Key",
    "delete_key_confirm": "Are you sure you want to delete this key?",
    "key_count": "{count} keys",
    "key_limit_message": "You've reached the maximum ({limit}) API keys for free accounts",
    "key_added": "Key added successfully",
    "key_deleted": "Key deleted",
    "key_invalid": "Invalid API key for this platform",
    "export_settings": "Export Settings & Conversations",
    "export_description": "Export all your conversations and settings as a JSON file",
    "export_excludes": "Export does not include API keys for security reasons",
    "export_button": "Export Data",
    "export_as_pdf": "Export as PDF",
    "export_as_json": "Export as JSON",
    "export_as_markdown": "Export as Markdown",
    "import_settings": "Import Settings",
    "import_replace": "Replace existing data",
    "import_merge": "Merge with existing data",
    "import_success": "Data imported successfully",
    "import_error": "Error importing data",
    "import_invalid_file": "Invalid file",
    "import_button": "Import Data",
    "saved": "Settings saved",
    "save_error": "Error saving settings"
  },
  "admin": {
    "dashboard": "Dashboard",
    "users": "Users",
    "api_keys": "API Keys",
    "models": "Models",
    "personas": "Personas",
    "shared_personas": "Shared Personas",
    "invite_codes": "Invite Codes",
    "notifications": "Notifications",
    "system_settings": "System Settings",
    "total_users": "Total Users",
    "active_today": "Active Today",
    "premium_accounts": "Premium Accounts",
    "total_conversations_stat": "Total Conversations",
    "messages_today": "Messages Today",
    "tokens_today": "Tokens Today",
    "top_personas": "Top Personas",
    "recent_notifications": "Recent Notifications",
    "recent_users": "Recent Users",
    "user_table_name": "Name",
    "user_table_email": "Email",
    "user_table_role": "Role",
    "user_table_joined": "Joined",
    "user_table_last_active": "Last Active",
    "user_table_status": "Status",
    "user_table_conversations": "Conversations",
    "user_table_messages": "Messages",
    "user_table_actions": "Actions",
    "upgrade_premium": "Upgrade to Premium",
    "downgrade_free": "Downgrade to Free",
    "upgrade_admin": "Make Admin",
    "downgrade_admin": "Remove Admin",
    "ban_user": "Ban User",
    "unban_user": "Unban User",
    "delete_user": "Delete User",
    "delete_user_confirm": "Are you sure you want to delete this user and all their data?",
    "delete_user_type": "Type DELETE to confirm",
    "set_duration": "Set Duration",
    "duration_days": "{days} days",
    "duration_permanent": "Permanent",
    "add_api_key": "Add Global API Key",
    "edit_key": "Edit Key",
    "delete_key_admin": "Delete Key",
    "toggle_active": "Toggle Active",
    "model_name": "Model Name",
    "model_id": "Model ID",
    "add_model": "Add Model",
    "auto_fetch": "Auto Fetch",
    "fetch_models": "Fetch Models",
    "fetching_models": "Fetching models...",
    "models_fetched": "{count} models fetched",
    "reorder": "Reorder",
    "add_system_persona": "Add System Persona",
    "add_premium_persona": "Add Premium Persona",
    "edit_persona": "Edit Persona",
    "delete_persona": "Delete Persona",
    "convert_to_system": "Convert to System",
    "cannot_delete_original": "Cannot delete original system personas",
    "pending_personas": "Personas Pending Approval",
    "approve": "Approve",
    "reject": "Reject",
    "preview_persona": "Preview Persona",
    "edit_before_approve": "Edit Before Approving",
    "no_pending": "No personas pending approval",
    "create_invite": "Create Invite Code",
    "code_label": "Code",
    "max_uses": "Max Uses",
    "premium_duration": "Premium Duration",
    "code_expiry": "Expiry Date",
    "generate_code": "Generate Code",
    "copy_link": "Copy Link",
    "link_copied": "Link copied",
    "deactivate_code": "Deactivate Code",
    "delete_code": "Delete Code",
    "view_uses": "View Uses",
    "mark_all_read": "Mark All as Read",
    "filter_by_type": "Filter by Type",
    "filter_by_priority": "Filter by Priority",
    "filter_by_status": "Filter by Status",
    "delete_notification": "Delete Notification",
    "delete_old": "Delete Old Notifications",
    "telegram_token": "Telegram Bot Token",
    "telegram_chat_id": "Telegram Chat ID",
    "test_connection": "Test Connection",
    "test_success": "Test message sent successfully",
    "test_failed": "Connection test failed",
    "notification_toggles": "Enable/Disable Notification Types",
    "save_settings": "Save Settings",
    "system_limits": "System Limits",
    "limit_free_messages": "Free messages before delay",
    "limit_free_delay": "Free account delay (seconds)",
    "limit_premium_delay": "Premium account delay (seconds)",
    "limit_message_per_chat": "Messages per chat limit",
    "limit_max_conversations": "Max conversations for free",
    "limit_max_api_keys": "Max API keys for free",
    "limit_max_personas": "Max personas for free",
    "limit_trial_days": "Trial duration (days)",
    "user_updated": "User updated",
    "user_deleted": "User deleted",
    "key_created": "Key created",
    "key_updated": "Key updated",
    "key_deleted": "Key deleted",
    "model_created": "Model added",
    "model_deleted": "Model deleted",
    "persona_created": "Persona created",
    "persona_updated": "Persona updated",
    "persona_deleted": "Persona deleted",
    "persona_approved": "Persona approved",
    "persona_rejected": "Persona rejected",
    "code_created": "Code created",
    "code_deactivated": "Code deactivated",
    "code_deleted": "Code deleted",
    "settings_saved": "Settings saved",
    "no_data": "No data available",
    "refresh": "Refresh"
  },
  "notifications": {
    "user_registered": "New user registered",
    "trial_requested": "Free trial requested",
    "trial_expired": "Trial period expired",
    "premium_expired": "Premium subscription expired",
    "persona_shared": "New shared persona",
    "api_low_balance": "Low API balance",
    "api_depleted": "API balance depleted",
    "system_error": "System error",
    "invite_code_used": "Invite code used"
  },
  "onboarding": {
    "step1_title": "Sidebar",
    "step1_message": "Here you'll find all your conversations organized by date and folders. You can create new folders and organize your chats easily.",
    "step2_title": "Top Bar",
    "step2_message": "Select the platform and model from here. You can switch between 7 different AI platforms.",
    "step3_title": "Personas",
    "step3_message": "Use ready-made personas specialized in different fields, or create your own to customize your chat experience.",
    "step4_title": "Quick Shortcuts",
    "step4_message": "Type / in the message box for quick access to built-in personas: /linkedin /brainstorm /prompt /email",
    "step5_title": "Settings & API Keys",
    "step5_message": "Add your own API keys from Settings for direct model access. Keys are encrypted with AES-256.",
    "step6_title": "Get Started!",
    "step6_message": "You're ready to start chatting. Select a model from the top bar and type your first message!",
    "skip": "Skip",
    "next": "Next",
    "previous": "Previous",
    "start_using": "Start Using"
  },
  "common": {
    "loading": "Loading...",
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "create": "Create",
    "copy": "Copy",
    "copied": "Copied!",
    "confirm": "Confirm",
    "yes": "Yes",
    "no": "No",
    "ok": "OK",
    "close": "Close",
    "search": "Search",
    "filter": "Filter",
    "sort": "Sort",
    "export_label": "Export",
    "import_label": "Import",
    "refresh": "Refresh",
    "back": "Back",
    "next_label": "Next",
    "previous_label": "Previous",
    "skip_label": "Skip",
    "done": "Done",
    "required": "Required",
    "optional": "Optional",
    "unlimited": "Unlimited",
    "permanent": "Permanent",
    "days": "days",
    "active": "Active",
    "inactive": "Inactive",
    "banned": "Banned",
    "all": "All",
    "no_results": "No results found",
    "error_occurred": "An error occurred",
    "try_again": "Try again",
    "unauthorized": "Unauthorized",
    "not_found": "Not found",
    "free": "Free",
    "premium": "Premium",
    "admin": "Admin",
    "online": "Online",
    "offline": "Offline"
  },
  "errors": {
    "generic": "An unexpected error occurred. Please try again.",
    "network": "Network connection error. Check your internet connection.",
    "unauthorized": "You are not authorized to access this page.",
    "not_found": "The requested page was not found.",
    "rate_limited": "Rate limit exceeded. Please wait a moment.",
    "limit_reached": "You've reached the maximum limit for your account.",
    "invalid_input": "Invalid input data. Check your entries and try again.",
    "banned_account": "Your account has been banned. Contact administration for more info.",
    "server_error": "Server error. Please try again later.",
    "api_key_invalid": "Invalid or expired API key.",
    "model_not_available": "The selected model is currently unavailable.",
    "conversation_not_found": "Conversation not found or has been deleted.",
    "persona_not_found": "Persona not found.",
    "file_too_large": "File is too large.",
    "unsupported_format": "Unsupported file format."
  }
}
""")

    # ──────────────────────────────────────────────
    # GROUP H: Root Layout (1 file)
    # ──────────────────────────────────────────────
    print("\n📁 Group H: Root Layout")
    print("-" * 40)

    # 13. app/[locale]/layout.tsx
    create_file("app/[locale]/layout.tsx", """// التخطيط الجذري: يغلف جميع الصفحات بإعدادات اللغة والخطوط والمظهر
// يدعم العربية (RTL) والإنجليزية (LTR) مع خطوط Cairo و Inter
import type { Metadata, Viewport } from 'next';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { Cairo, Inter } from 'next/font/google';
import { notFound } from 'next/navigation';
import '@/app/globals.css';

/**
 * خط Cairo للعربية
 */
const cairo = Cairo({
  subsets: ['arabic', 'latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-cairo',
  display: 'swap',
});

/**
 * خط Inter للإنجليزية
 */
const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-inter',
  display: 'swap',
});

/**
 * اللغات المدعومة
 */
const locales = ['ar', 'en'] as const;

/**
 * البيانات الوصفية للتطبيق
 */
export const metadata: Metadata = {
  title: {
    default: process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat Platform',
    template: `%s | ${process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat Platform'}`,
  },
  description: 'Professional Multi-Platform AI Chat Platform with Personas - منصة دردشة احترافية متعددة المنصات بالذكاء الاصطناعي',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/icons/icon-192x192.png',
  },
  openGraph: {
    title: process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat Platform',
    description: 'Professional Multi-Platform AI Chat Platform with Personas',
    url: process.env.NEXT_PUBLIC_APP_URL ?? 'https://localhost:3000',
    siteName: process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat Platform',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat Platform',
    description: 'Professional Multi-Platform AI Chat Platform with Personas',
  },
  robots: {
    index: true,
    follow: true,
  },
};

/**
 * إعدادات العرض
 */
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: '#6c63ff',
};

/**
 * واجهة خصائص التخطيط
 */
interface RootLayoutProps {
  children: React.ReactNode;
  params: { locale: string };
}

/**
 * توليد المسارات الثابتة للغات
 */
export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

/**
 * التخطيط الجذري للتطبيق
 * يتعامل مع اللغة والاتجاه والخطوط والمظهر
 */
export default async function RootLayout({
  children,
  params: { locale },
}: RootLayoutProps) {
  // التحقق من صحة اللغة
  if (!locales.includes(locale as typeof locales[number])) {
    notFound();
  }

  // تحميل رسائل الترجمة
  const messages = await getMessages();

  // تحديد الاتجاه بناءً على اللغة
  const direction = locale === 'ar' ? 'rtl' : 'ltr';

  // تحديد الخط الرئيسي بناءً على اللغة
  const fontVariable = locale === 'ar' ? cairo.variable : inter.variable;
  const fontClass = locale === 'ar' ? 'font-sans-arabic' : 'font-sans';

  return (
    <html
      lang={locale}
      dir={direction}
      className={`dark ${cairo.variable} ${inter.variable}`}
      suppressHydrationWarning
    >
      <head>
        <meta charSet="utf-8" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body
        className={`${fontClass} min-h-screen bg-white dark:bg-dark-950 text-gray-900 dark:text-gray-100 antialiased`}
        suppressHydrationWarning
      >
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
""")

    # ──────────────────────────────────────────────
    # BONUS: Create page.tsx for locale root (redirect to chat)
    # ──────────────────────────────────────────────
    create_file("app/[locale]/page.tsx", """// الصفحة الرئيسية: تعيد توجيه المستخدم إلى صفحة الدردشة
import { redirect } from 'next/navigation';

/**
 * خصائص الصفحة الرئيسية
 */
interface HomePageProps {
  params: { locale: string };
}

/**
 * الصفحة الرئيسية - إعادة توجيه تلقائية لصفحة الدردشة
 */
export default function HomePage({ params: { locale } }: HomePageProps) {
  redirect(`/${locale}/chat`);
}
""")

    # ──────────────────────────────────────────────
    # BONUS: next-intl navigation config
    # ──────────────────────────────────────────────
    create_file("i18n/navigation.ts", """// إعدادات التنقل مع next-intl: تصدير دوال التنقل المحلية
import { createSharedPathnamesNavigation } from 'next-intl/navigation';

/**
 * اللغات المدعومة
 */
export const locales = ['ar', 'en'] as const;

/**
 * بادئة اللغة في المسار
 */
export const localePrefix = 'always' as const;

/**
 * دوال التنقل المحلية
 * Link: رابط مع دعم اللغة
 * redirect: إعادة توجيه مع دعم اللغة
 * usePathname: مسار الصفحة الحالية
 * useRouter: موجه مع دعم اللغة
 */
export const { Link, redirect, usePathname, useRouter } =
  createSharedPathnamesNavigation({ locales, localePrefix });
""")

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 1B SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print("  GROUP E - Supabase Clients:")
    print("    1.  lib/supabase-client.ts     (Browser client - Singleton)")
    print("    2.  lib/supabase-server.ts      (Server client - Cookie-based)")
    print("    3.  lib/supabase-admin.ts       (Admin client - Service Role)")
    print()
    print("  GROUP F - Zustand Stores:")
    print("    4.  stores/authStore.ts         (Auth state - NO persist)")
    print("    5.  stores/chatStore.ts         (Chat state - NO persist)")
    print("    6.  stores/uiStore.ts           (UI state - WITH persist)")
    print("    7.  stores/personaStore.ts      (Persona state - WITH persist)")
    print("    8.  stores/platformStore.ts     (Platform state - WITH persist)")
    print("    9.  stores/settingsStore.ts     (Settings state - WITH persist)")
    print()
    print("  GROUP G - Internationalization:")
    print("    10. i18n/config.ts              (next-intl config)")
    print("    11. i18n/ar.json                (Arabic translations - COMPLETE)")
    print("    12. i18n/en.json                (English translations - COMPLETE)")
    print("    +   i18n/navigation.ts          (Shared navigation helpers)")
    print()
    print("  GROUP H - Root Layout:")
    print("    13. app/[locale]/layout.tsx      (Root layout with RTL/LTR)")
    print("    +   app/[locale]/page.tsx        (Home redirect to /chat)")
    print()
    print("📝 NOTES:")
    print("  - All files have Arabic comments at top")
    print("  - No 'any' type used anywhere (TypeScript strict)")
    print("  - Supabase clients: browser (singleton), server (cookie), admin (service)")
    print("  - Zustand stores: auth/chat (no persist), ui/persona/platform/settings (persist)")
    print("  - i18n: ~300+ translation keys covering ALL app sections")
    print("  - Layout: Cairo font for Arabic, Inter for English, RTL/LTR automatic")
    print("  - Dark mode enabled by default via 'dark' class on <html>")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 2:  Authentication (login, register, route guard, useAuth hook)")
    print("  Phase 3A: Chat core (API route, providers, encryption)")
    print("  Phase 3B: Chat UI (sidebar, header, message components)")
    print("  Phase 3C: Chat features (streaming, slash commands, rate limiting)")
    print("  Phase 4:  API Keys management")
    print("  Phase 5A: Features (personas, folders)")
    print("  Phase 5B: Features (favorites, export, onboarding)")
    print("  Phase 6A: Admin panel (layout, dashboard, users)")
    print("  Phase 6B: Admin panel (keys, models, personas, codes, notifications)")
    print("  Phase 7:  Final (worker proxy, telegram, polish)")
    print()
    print("✅ Phase 1B Complete! Ready for Phase 2.")


if __name__ == "__main__":
    main()
